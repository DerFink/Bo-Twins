<?php
/* Gasballon-Simulator: Dienst für die gemeinsame Bestenliste (SRV-02 bis SRV-04)
   Braucht PHP 8 mit PDO-SQLite und Schreibrecht auf den Unterordner "data". Keine weiteren Pakete.
   Gespeichert werden: Name, Aufgabe, Punkte bzw. km, Restsand, Dauer, Zeitpunkt, Build und ein Kurzwert der
   zufälligen Gerätekennung (nicht die Kennung selbst). Keine IP-Adresse, kein Standort.

   Aufrufe
     GET  ?action=check                   Selbsttest ohne Datenbank: PHP-Version, Erweiterungen, Schreibrecht (immer Status 200, damit der Server die Antwort nicht durch seine Fehlerseite ersetzt)
     GET  ?action=ping                    Lebenszeichen
     GET  ?action=top&kind=chal|gb        Liste (chal: höchstens 100, gb: höchstens 500)
     POST ?action=score                   Ergebnis melden (JSON als Text)
     POST ?action=unscore                 eigenes Ergebnis zurückziehen (Meisterschaft: „30 Minuten noch einmal“)
     POST ?action=visit / ?action=leave   Besuch und Nutzungsdauer zählen
     GET  ?action=pubstats                öffentliche Statistik: Zahl der Geräte und Verteilung der Nutzungszeit je Gerät (nur Summen, keine Einzelwerte)
     GET  ?action=admin&key=…             letzte 200 Einträge mit Nummer
     GET  ?action=delete&key=…&id=…       Eintrag löschen
     GET  ?action=stats&key=…             Besuche je Tag
     GET  ?action=testmail&key=…          Probenachricht an den Admin schicken und das Ergebnis zeigen
   Nachrichten an den Admin (SRV-08): Ist in config.php ein Empfänger eingetragen, schickt der Dienst eine E-Mail, wenn eine Liste zu 80 % oder
   ganz gefüllt ist, bei Meilensteinen der Gerätezahl, bei auffälligen Meldungen eines Geräts und wenn die Datenbank nicht schreibbar ist.
   Jede Nachricht geht nur einmal hinaus.
   Der Schlüssel für die Verwaltung steht in config.php. */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

$CFG = ['admin_key' => '', 'max_per_hour' => 60, 'keep_visits_days' => 400, 'notify_to' => '', 'notify_from' => '', 'site_name' => 'Gasballon-Simulator',
        'smtp_host' => '', 'smtp_port' => 587, 'smtp_user' => '', 'smtp_pass' => '', 'smtp_secure' => 'tls'];
if (is_file(__DIR__ . '/config.php')) { $c = include __DIR__ . '/config.php'; if (is_array($c)) $CFG = array_merge($CFG, $c); }

/* ---------- Nachrichten an den Admin ---------- */
function smtpSend(array $C, string $to, string $from, string $subject, string $body, ?string &$err = null): bool {
  $sec = strtolower((string)$C['smtp_secure']); $host = ($sec === 'ssl' ? 'ssl://' : '') . $C['smtp_host'];
  $fp = @stream_socket_client($host . ':' . (int)$C['smtp_port'], $en, $es, 12); if (!$fp) { $err = 'keine Verbindung: ' . $es; return false; }
  stream_set_timeout($fp, 12);
  $get = function () use ($fp) { $r = ''; while (($l = fgets($fp, 600)) !== false) { $r .= $l; if (strlen($l) < 4 || $l[3] === ' ') break; } return $r; };
  $cmd = function (string $c, string $ok) use ($fp, $get, &$err) { fwrite($fp, $c . "\r\n"); $r = $get(); if (strncmp($r, $ok, strlen($ok)) !== 0) { $err = trim(preg_replace('/^AUTH.*|^[A-Za-z0-9+\/=]{16,}$/', '…', $c)) . ' -> ' . trim($r); return false; } return true; };
  $me = preg_replace('/[^A-Za-z0-9.-]/', '', (string)($_SERVER['SERVER_NAME'] ?? 'localhost')) ?: 'localhost';
  $r = $get(); if (strncmp($r, '220', 3) !== 0) { $err = 'Begrüßung: ' . trim($r); fclose($fp); return false; }
  $ok = $cmd('EHLO ' . $me, '250');
  if ($ok && $sec === 'tls') { $ok = $cmd('STARTTLS', '220') && @stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT) && $cmd('EHLO ' . $me, '250'); if (!$ok && !$err) $err = 'TLS ließ sich nicht aufbauen'; }
  if ($ok && $C['smtp_user'] !== '') $ok = $cmd('AUTH LOGIN', '334') && $cmd(base64_encode((string)$C['smtp_user']), '334') && $cmd(base64_encode((string)$C['smtp_pass']), '235');
  $ok = $ok && $cmd('MAIL FROM:<' . $from . '>', '250') && $cmd('RCPT TO:<' . $to . '>', '25') && $cmd('DATA', '354');
  if ($ok) {
    $msg = 'From: ' . $from . "\r\nTo: " . $to . "\r\nSubject: =?UTF-8?B?" . base64_encode($subject) . "?=\r\nDate: " . date('r') . "\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($body));
    $ok = $cmd($msg . "\r\n.", '250');
  }
  @fwrite($fp, "QUIT\r\n"); fclose($fp); return (bool)$ok;
}
function sendMail(array $C, string $subject, string $body, ?string &$err = null): bool {
  $to = trim((string)$C['notify_to']); if ($to === '' || !filter_var($to, FILTER_VALIDATE_EMAIL)) { $err = 'kein gültiger Empfänger in config.php (notify_to)'; return false; }
  $from = trim((string)$C['notify_from']); if ($from === '' || !filter_var($from, FILTER_VALIDATE_EMAIL)) $from = $C['smtp_user'] !== '' && filter_var($C['smtp_user'], FILTER_VALIDATE_EMAIL) ? $C['smtp_user'] : $to;
  $subject = '[' . $C['site_name'] . '] ' . $subject; $body .= "\n\n-- \n" . $C['site_name'] . ' auf ' . ($_SERVER['HTTP_HOST'] ?? 'dem Server') . ', ' . date('d.m.Y H:i') . "\nDiese Nachricht kommt nur einmal je Anlass.";
  if ($C['smtp_host'] !== '') return smtpSend($C, $to, $from, $subject, $body, $err);
  $ok = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, "From: $from\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8");
  if (!$ok) $err = 'mail() meldet einen Fehler: Auf dem Server ist kein Mailversand eingerichtet. Abhilfe: SMTP-Zugang in config.php eintragen.';
  return $ok;
}
/* Einmalige Nachricht: Der Schlüssel wird in der Datenbank vermerkt, damit derselbe Anlass nicht zweimal meldet. */
function notify(array $C, string $key, string $subject, string $body): void {
  if (trim((string)$C['notify_to']) === '') return;
  try {
    $pdo = db(); $q = $pdo->prepare('INSERT OR IGNORE INTO notes (k, at, ok) VALUES (?,?,0)'); $q->execute([$key, nowMs()]); if ($q->rowCount() < 1) return;
    $ok = sendMail($C, $subject, $body, $err); $pdo->prepare('UPDATE notes SET ok = ?, err = ? WHERE k = ?')->execute([$ok ? 1 : 0, $ok ? null : substr((string)$err, 0, 200), $key]);
  } catch (Throwable $e) { error_log('gasballon notify: ' . $e->getMessage()); }
}
/* Datenbank nicht schreibbar: höchstens einmal am Tag melden; der Merker liegt im Temp-Ordner, weil die Datenbank ja gerade fehlt. */
function alarmNoDb(array $C, string $why): void {
  if (trim((string)$C['notify_to']) === '') return; $f = sys_get_temp_dir() . '/gasballon_dbalarm_' . md5(__DIR__);
  if (is_file($f) && time() - filemtime($f) < 86400) return; @touch($f);
  sendMail($C, 'Datenbank nicht schreibbar', "Der Dienst für die Bestenliste kann seine Daten nicht speichern.\nGrund: $why\n\nPrüfen: Hat der Webserver (Gruppe http) Schreibrecht im Ordner api und im Unterordner data? Ist die Platte voll?");
}

function out($x, int $code = 200): void { http_response_code($code); echo json_encode($x, JSON_UNESCAPED_UNICODE); exit; }
function fail(string $why, int $code = 400): void { out(['ok' => false, 'error' => $why], $code); }

/* Datenbank: Der Dateiname enthält einen Zufallswert, damit die Datei nicht über den Browser abrufbar ist,
   auch wenn der Server (zum Beispiel nginx) die .htaccess im Ordner "data" nicht beachtet. */
function db(): PDO {
  static $pdo = null; if ($pdo) return $pdo;
  $dir = __DIR__ . '/data';
  if (!is_dir($dir) && !@mkdir($dir, 0770, true)) { alarmNoDb($GLOBALS['CFG'], 'Ordner data fehlt und lässt sich nicht anlegen'); fail('Ordner data fehlt und lässt sich nicht anlegen', 500); }
  if (!is_writable($dir)) { alarmNoDb($GLOBALS['CFG'], 'Ordner data ist nicht beschreibbar'); fail('Ordner data ist nicht beschreibbar', 500); }
  $keyFile = $dir . '/key.php';
  if (!is_file($keyFile)) {
    $k = ['file' => 'gb_' . bin2hex(random_bytes(16)) . '.sqlite', 'salt' => bin2hex(random_bytes(16))];
    file_put_contents($keyFile, '<?php return ' . var_export($k, true) . ';', LOCK_EX);
    if (!is_file($dir . '/.htaccess')) @file_put_contents($dir . '/.htaccess', "Require all denied\n");
    if (!is_file($dir . '/index.html')) @file_put_contents($dir . '/index.html', '');
  }
  $k = include $keyFile; $GLOBALS['SALT'] = $k['salt'];
  $pdo = new PDO('sqlite:' . $dir . '/' . $k['file'], null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
  $pdo->exec('PRAGMA journal_mode=WAL; PRAGMA busy_timeout=4000;');
  $pdo->exec('CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, dev TEXT NOT NULL, n TEXT NOT NULL, c TEXT NOT NULL, l INTEGER, p REAL NOT NULL, s REAL, t INTEGER, km REAL, rank INTEGER, dq TEXT, build TEXT, cat INTEGER, at INTEGER NOT NULL)');
  $pdo->exec('CREATE INDEX IF NOT EXISTS scores_c ON scores (c, p DESC)');
  $pdo->exec('CREATE INDEX IF NOT EXISTS scores_dev ON scores (dev, at)');
  $pdo->exec('CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY AUTOINCREMENT, day TEXT NOT NULL, dev TEXT NOT NULL, src TEXT, ref TEXT, lang TEXT, build TEXT, sec INTEGER DEFAULT 0, at INTEGER NOT NULL)');
  $pdo->exec('CREATE INDEX IF NOT EXISTS visits_day ON visits (day)');
  $pdo->exec('CREATE TABLE IF NOT EXISTS notes (k TEXT PRIMARY KEY, at INTEGER NOT NULL, ok INTEGER DEFAULT 0, err TEXT)');
  return $pdo;
}
function dev(mixed $id): string { $id = is_string($id) ? substr($id, 0, 80) : ''; if ($id === '') fail('Kennung fehlt'); return substr(hash('sha256', $GLOBALS['SALT'] . '|' . $id), 0, 24); }
function body(): array {
  $raw = file_get_contents('php://input', false, null, 0, 4096); $j = json_decode($raw ?: '', true);
  if (!is_array($j)) fail('kein gültiges JSON'); return $j;
}
function txt(mixed $v, int $max): string {
  $s = is_string($v) ? $v : ''; $s = preg_replace('/[\x00-\x1F\x7F<>]/u', '', $s) ?? ''; $s = trim(preg_replace('/\s+/u', ' ', $s) ?? '');
  return function_exists('mb_substr') ? mb_substr($s, 0, $max) : substr($s, 0, $max * 3);
}
function num(mixed $v, float $lo, float $hi, ?float $def = null): ?float { if (!is_int($v) && !is_float($v)) return $def; if (is_nan((float)$v) || $v < $lo || $v > $hi) return $def; return (float)$v; }
function admin(array $CFG): void { $k = (string)($_GET['key'] ?? ''); if ($CFG['admin_key'] === '' || strlen($CFG['admin_key']) < 12 || !hash_equals($CFG['admin_key'], $k)) fail('nicht erlaubt', 403); }
function nowMs(): int { return (int)floor(microtime(true) * 1000); }

$action = (string)($_GET['action'] ?? '');
if ($action === 'check') {                       // Selbsttest (SRV-09): sagt, was fehlt, ohne die Datenbank anzufassen
  $dir = __DIR__ . '/data'; $ext = []; foreach (['pdo_sqlite', 'sqlite3', 'openssl', 'mbstring', 'json'] as $e) $ext[$e] = extension_loaded($e);
  $w = is_dir($dir) ? is_writable($dir) : is_writable(__DIR__); $hint = [];
  if (PHP_VERSION_ID < 80000) $hint[] = 'PHP 8.0 oder neuer wählen (jetzt ' . PHP_VERSION . ').';
  if (!$ext['pdo_sqlite']) $hint[] = 'Im PHP-Profil der Web Station die Erweiterung pdo_sqlite ankreuzen.';
  if (!$w) $hint[] = 'Der Webserver (Gruppe http) braucht Lesen und Schreiben im Ordner api, auch für Unterordner.';
  if (!$ext['openssl']) $hint[] = 'Nur für E-Mail-Nachrichten: Erweiterung openssl ankreuzen.';
  $db = null; if (!$hint || (count($hint) === 1 && !$ext['openssl'])) { try { db(); $db = true; } catch (Throwable $e) { $db = $e->getMessage(); } }
  http_response_code(200); echo json_encode(['check' => true, 'php' => PHP_VERSION, 'erweiterungen' => $ext, 'ordner_api_schreibbar' => $w, 'ordner_data_vorhanden' => is_dir($dir), 'datenbank' => $db, 'benutzer' => function_exists('posix_geteuid') && function_exists('posix_getpwuid') ? (posix_getpwuid(posix_geteuid())['name'] ?? null) : get_current_user(), 'zu_tun' => $hint ?: ['nichts, alles in Ordnung']], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT); exit;
}
try {
  switch ($action) {
    case 'ping':
      db(); out(['ok' => true, 'v' => 1]);

    case 'top': {
      $kind = (string)($_GET['kind'] ?? 'chal');
      if ($kind === 'gb') {
        $r = db()->query("SELECT n, km, rank, dq, t, at FROM scores WHERE c = 'gb69' ORDER BY (dq IS NOT NULL), km DESC, at ASC LIMIT 500")->fetchAll();
        foreach ($r as &$x) { $x['km'] = (float)$x['km']; $x['rank'] = $x['rank'] === null ? null : (int)$x['rank']; $x['t'] = (int)$x['t']; $x['at'] = (int)$x['at']; }
        out($r);
      }
      $r = db()->query("SELECT n, p, c, l, s, at FROM scores WHERE c <> 'gb69' ORDER BY p DESC, s DESC, at ASC LIMIT 100")->fetchAll();
      foreach ($r as &$x) { $x['p'] = (float)$x['p'] + 0; if ($x['p'] == floor($x['p'])) $x['p'] = (int)$x['p']; $x['l'] = $x['l'] === null ? null : (int)$x['l']; $x['s'] = (float)$x['s']; $x['at'] = (int)$x['at']; }
      out($r);
    }

    case 'score': {
      if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('nur POST', 405);
      $j = body(); $pdo = db(); $d = dev($j['id'] ?? null); $now = nowMs();
      $c = (string)($j['c'] ?? ''); if (!in_array($c, ['target', 'wz', 'mdt', 'mid', 'gb69'], true)) fail('Aufgabe unbekannt');
      $n = txt($j['n'] ?? '', 24); if ($n === '') $n = 'Pilot';
      $q = $pdo->prepare('SELECT COUNT(*) FROM scores WHERE dev = ? AND at > ?'); $q->execute([$d, $now - 3600000]);
      if ((int)$q->fetchColumn() >= (int)$CFG['max_per_hour']) fail('zu viele Meldungen', 429);
      $t = num($j['t'] ?? null, 0, 400000, 0); $s = num($j['s'] ?? null, 0, 5000, 0); $cat = num($j['at'] ?? null, 0, 9e15, 0);
      if ($c === 'gb69') {
        $km = num($j['km'] ?? null, 0, 6000); if ($km === null) fail('km fehlt');
        $dq = $j['dq'] ?? null; if ($dq !== null && !in_array($dq, ['zone', 'water', 'hard'], true)) fail('Grund unbekannt');
        $rank = $dq === null ? num($j['rank'] ?? null, 1, 1000) : null;
        $pdo->prepare('INSERT INTO scores (dev, n, c, l, p, s, t, km, rank, dq, build, cat, at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)')
            ->execute([$d, $n, $c, null, round($km), $s, (int)$t, round($km, 2), $rank === null ? null : (int)$rank, $dq, txt($j['build'] ?? '', 20), (int)$cat, $now]);
      } else {
        $p = num($j['p'] ?? null, 0, 100); if ($p === null) fail('Punkte fehlen oder außerhalb 0 bis 100');
        $l = $c === 'target' ? num($j['l'] ?? null, 0, 2) : null;
        $pdo->prepare('INSERT INTO scores (dev, n, c, l, p, s, t, km, rank, dq, build, cat, at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)')
            ->execute([$d, $n, $c, $l === null ? null : (int)$l, round($p, 1), round($s, 1), (int)$t, null, null, null, txt($j['build'] ?? '', 20), (int)$cat, $now]);
      }
      /* Nachrichten an den Admin: Füllstand der Listen und auffällige Geräte */
      if (trim((string)$CFG['notify_to']) !== '') {
        if ($c === 'gb69') { $nG = (int)$pdo->query("SELECT COUNT(*) FROM scores WHERE c = 'gb69'")->fetchColumn();
          if ($nG >= 500) notify($CFG, 'gb-500', 'Liste „69. Gordon Bennett“ ist voll', "Die Liste hat $nG Einträge. Angezeigt werden die 500 weitesten Fahrten; schwächere fallen ab jetzt aus der Anzeige. Gespeichert bleibt alles.");
          elseif ($nG >= 400) notify($CFG, 'gb-400', 'Liste „69. Gordon Bennett“ zu 80 % gefüllt', "Die Liste hat $nG von 500 angezeigten Einträgen.");
          if (($km ?? 0) > 2000) notify($CFG, 'far-' . $d . '-' . gmdate('Ymd'), 'Auffällig weite Fahrt', "Ein Gerät meldet $km km in der Meisterschaft (Name: $n). Das ist weiter, als das Wetter des Rennens plausibel hergibt.\nPrüfen und bei Bedarf löschen: api.php?action=admin&key=…");
        } else { $nC = (int)$pdo->query("SELECT COUNT(*) FROM scores WHERE c <> 'gb69'")->fetchColumn();
          if ($nC >= 100) notify($CFG, 'chal-100', 'Bestenliste der Challenges ist voll', "Es gibt $nC gewertete Fahrten. Angezeigt werden die besten 100.");
          elseif ($nC >= 80) notify($CFG, 'chal-80', 'Bestenliste der Challenges zu 80 % gefüllt', "Es gibt $nC von 100 angezeigten Einträgen.");
          $q = $pdo->prepare("SELECT COUNT(*) FROM scores WHERE dev = ? AND c <> 'gb69' AND p >= 100 AND at > ?"); $q->execute([$d, $now - 86400000]);
          if ((int)$q->fetchColumn() >= 5) notify($CFG, 'top-' . $d . '-' . gmdate('Ymd'), 'Auffällig viele volle Punktzahlen', "Ein Gerät hat in 24 Stunden mindestens fünfmal 100 Punkte gemeldet (Name zuletzt: $n).\nPrüfen und bei Bedarf löschen: api.php?action=admin&key=…");
        }
        $q = $pdo->prepare('SELECT COUNT(*) FROM scores WHERE dev = ? AND at > ?'); $q->execute([$d, $now - 3600000]);
        if ((int)$q->fetchColumn() >= max(10, (int)$CFG['max_per_hour'] / 2)) notify($CFG, 'many-' . $d . '-' . gmdate('Ymd'), 'Auffällig viele Meldungen von einem Gerät', "Ein Gerät hat in einer Stunde sehr viele Ergebnisse gemeldet (Name zuletzt: $n). Ab " . (int)$CFG['max_per_hour'] . " je Stunde weist der Dienst weitere ab.");
      }
      out(['ok' => true]);
    }

    case 'unscore': {
      if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('nur POST', 405);
      $j = body(); $pdo = db(); $d = dev($j['id'] ?? null); $cat = num($j['at'] ?? null, 1, 9e15); if ($cat === null) fail('Zeitpunkt fehlt');
      $q = $pdo->prepare('DELETE FROM scores WHERE dev = ? AND cat = ?'); $q->execute([$d, (int)$cat]); out(['ok' => true, 'n' => $q->rowCount()]);
    }

    case 'visit': {
      if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('nur POST', 405);
      $j = body(); $pdo = db(); $d = dev($j['id'] ?? null); $now = nowMs();
      $q = $pdo->prepare('SELECT COUNT(*) FROM visits WHERE dev = ? AND at > ?'); $q->execute([$d, $now - 3600000]);
      if ((int)$q->fetchColumn() < 30) $pdo->prepare('INSERT INTO visits (day, dev, src, ref, lang, build, at) VALUES (?,?,?,?,?,?,?)')->execute([gmdate('Y-m-d'), $d, txt($j['src'] ?? '', 40), txt($j['ref'] ?? '', 80), txt($j['lang'] ?? '', 8), txt($j['build'] ?? '', 20), $now]);
      if (trim((string)$CFG['notify_to']) !== '') { $nU = (int)$pdo->query('SELECT COUNT(DISTINCT dev) FROM visits')->fetchColumn(); foreach ([1000, 500, 100, 50, 10] as $m) if ($nU >= $m) { notify($CFG, 'users-' . $m, "$m Geräte haben die App geöffnet", "Die App wurde bisher auf $nU Geräten geöffnet."); break; } }
      if (random_int(1, 50) === 1) $pdo->prepare('DELETE FROM visits WHERE at < ?')->execute([$now - (int)$CFG['keep_visits_days'] * 86400000]);
      out(['ok' => true]);
    }

    case 'leave': {
      if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('nur POST', 405);
      $j = body(); $pdo = db(); $d = dev($j['id'] ?? null); $sec = num($j['sec'] ?? null, 0, 86400, 0);
      $pdo->prepare('UPDATE visits SET sec = ? WHERE id = (SELECT id FROM visits WHERE dev = ? ORDER BY at DESC LIMIT 1)')->execute([(int)$sec, $d]);
      out(['ok' => true]);
    }

    case 'pubstats': {
      /* Öffentliche Statistik (SRV-07): je Gerät die Summe der Nutzungszeit, daraus Kennwerte. Es verlassen nur Summen und Kennwerte den Server. */
      $pdo = db(); $now = nowMs();
      $rows = $pdo->query('SELECT dev, SUM(sec) AS s, MIN(at) AS a0, MAX(at) AS a1 FROM visits GROUP BY dev')->fetchAll();
      $t = []; $u7 = 0; $first = null;
      foreach ($rows as $r) { if ((int)$r['a1'] > $now - 7 * 86400000) $u7++; if ($first === null || (int)$r['a0'] < $first) $first = (int)$r['a0']; if ((int)$r['s'] >= 30) $t[] = (int)$r['s']; }   // unter 30 s: nur geöffnet, zählt als Gerät, aber nicht für die Zeiten
      sort($t); $n = count($t);
      $q = function (float $f) use ($t, $n) { if ($n === 0) return 0; $x = $f * ($n - 1); $i = (int)floor($x); $j = min($n - 1, $i + 1); return (int)round($t[$i] + ($t[$j] - $t[$i]) * ($x - $i)); };
      $edges = [300, 900, 1800, 3600, 3 * 3600, 10 * 3600]; $hist = array_fill(0, count($edges) + 1, 0);
      foreach ($t as $v) { $k = 0; while ($k < count($edges) && $v >= $edges[$k]) $k++; $hist[$k]++; }
      $flights = (int)$pdo->query('SELECT COUNT(*) FROM scores')->fetchColumn();
      out(['ok' => true, 'users' => count($rows), 'users7' => $u7, 'timed' => $n, 'low' => $q(0.10), 'q1' => $q(0.25), 'median' => $q(0.50), 'q3' => $q(0.75), 'mean' => $n ? (int)round(array_sum($t) / $n) : 0, 'max' => $n ? $t[$n - 1] : 0,
           'sum' => array_sum($t), 'hist' => $hist, 'edges' => $edges, 'flights' => $flights, 'since' => $first, 'days' => (int)$CFG['keep_visits_days']]);
    }

    case 'admin': {
      admin($CFG);
      out(db()->query('SELECT id, n, c, l, p, s, km, rank, dq, build, dev, at FROM scores ORDER BY at DESC LIMIT 200')->fetchAll());
    }
    case 'delete': {
      admin($CFG); $id = (int)($_GET['id'] ?? 0); if ($id < 1) fail('Nummer fehlt');
      $q = db()->prepare('DELETE FROM scores WHERE id = ?'); $q->execute([$id]); out(['ok' => true, 'n' => $q->rowCount()]);
    }
    case 'stats': {
      admin($CFG);
      out(db()->query('SELECT day, COUNT(*) AS besuche, COUNT(DISTINCT dev) AS geraete, ROUND(AVG(NULLIF(sec, 0))) AS sekunden_im_mittel FROM visits GROUP BY day ORDER BY day DESC LIMIT 120')->fetchAll());
    }
    case 'testmail': {
      admin($CFG); $err = null; $ok = sendMail($CFG, 'Probenachricht', 'Wenn du das liest, funktioniert der Versand der Nachrichten an den Admin.', $err);
      out(['ok' => $ok, 'an' => $CFG['notify_to'], 'weg' => $CFG['smtp_host'] !== '' ? 'SMTP ' . $CFG['smtp_host'] . ':' . (int)$CFG['smtp_port'] : 'mail() des Servers', 'fehler' => $ok ? null : $err, 'gesendet' => db()->query('SELECT k, at, ok, err FROM notes ORDER BY at DESC LIMIT 30')->fetchAll()]);
    }
    default: fail('Aufruf unbekannt', 404);
  }
} catch (Throwable $e) {
  error_log('gasballon api: ' . $e->getMessage()); if (stripos($e->getMessage(), 'readonly') !== false || stripos($e->getMessage(), 'unable to open') !== false || stripos($e->getMessage(), 'disk') !== false) alarmNoDb($CFG, $e->getMessage());
  fail('Fehler im Dienst', 500);
}
