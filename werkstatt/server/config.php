<?php
/* Einstellungen des Dienstes. Diese Datei gibt beim Aufruf im Browser nichts aus. */
return [
  // Schlüssel für die Verwaltung (Einträge ansehen und löschen, Statistik, Probenachricht). Mindestens 12 Zeichen; leer = Verwaltung aus.
  'admin_key' => '',
  // höchstens so viele Ergebnisse je Gerät und Stunde
  'max_per_hour' => 60,
  // Besuchszählung so viele Tage aufbewahren
  'keep_visits_days' => 400,

  // ---- Nachrichten an den Admin (leer = keine Nachrichten) ----
  // Empfänger: an diese Adresse gehen die Nachrichten
  'notify_to' => '',
  // Absender; leer = das SMTP-Konto bzw. der Empfänger
  'notify_from' => '',
  // Name im Betreff
  'site_name' => 'Gasballon-Simulator',
  // Versand über ein Postfach (empfohlen). Bleibt smtp_host leer, versucht der Dienst es mit dem Mailversand des Servers (mail()).
  'smtp_host' => '',        // zum Beispiel mail.gmx.net
  'smtp_port' => 587,       // 587 mit 'tls', 465 mit 'ssl'
  'smtp_secure' => 'tls',   // 'tls' (STARTTLS), 'ssl' oder '' (unverschlüsselt, nur im eigenen Netz)
  'smtp_user' => '',        // Anmeldename des Postfachs, meist die Adresse
  'smtp_pass' => '',        // Kennwort des Postfachs; bei manchen Anbietern ein eigenes App-Kennwort
];
