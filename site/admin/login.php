<?php
require __DIR__ . '/../inc/bootstrap.php';
require __DIR__ . '/_ui.php';
start_session();
if (current_user()) { header('Location: index.php'); exit; }
$err = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  csrf_check();
  $email = strtolower(trim(isset($_POST['email']) ? (string)$_POST['email'] : ''));
  $pass = isset($_POST['password']) ? (string)$_POST['password'] : '';
  $ip = client_ip();
  if (login_blocked($ip, $email)) {
    http_response_code(429);
    $err = 'محاولات كثيرة. حاول مرة أخرى بعد 15 دقيقة.';
  } else {
    $st = db()->prepare('SELECT id, password_hash FROM pc_users WHERE email = ? LIMIT 1');
    $st->execute(array($email));
    $u = $st->fetch();
    // temps constant : on vérifie toujours un hachage, même si l'e-mail n'existe pas
    $hash = $u ? $u['password_hash'] : '$2y$12$azZRCgkckKfnIzQ4MKr1Z..R5BQDe4HtqAoRtBuUCAvUtE3RFxLYS';
    $ok = password_verify($pass, $hash) && $u;
    if ($ok) {
      login_cleared($ip, $email);
      session_regenerate_id(true);
      $_SESSION['uid'] = (int)$u['id'];
      $_SESSION['csrf'] = bin2hex(random_bytes(32));
      if (password_needs_rehash($u['password_hash'], PASSWORD_BCRYPT, array('cost' => 12))) db()->prepare('UPDATE pc_users SET password_hash = ? WHERE id = ?')->execute(array(hash_pw($pass), $u['id']));
      db()->prepare('UPDATE pc_users SET last_login = UTC_TIMESTAMP() WHERE id = ?')->execute(array($u['id']));
      header('Location: index.php'); exit;
    }
    login_failed($ip, $email);
    usleep(400000);
    $err = 'البريد الإلكتروني أو كلمة السر غير صحيحة.';
  }
}
ui_head('تسجيل الدخول', 'lg');
echo '<main class="lgc"><form method="post" class="lgf" autocomplete="on"><img src="../img/logo.webp" alt="Perfect Conseil" width="220" height="49"><h1>تسجيل الدخول</h1>'
  . ($err ? '<div class="al bad" role="alert">' . e($err) . '</div>' : '')
  . csrf_field()
  . '<label for="email">البريد الإلكتروني</label><input id="email" name="email" type="email" required autocomplete="username" dir="ltr" maxlength="190">'
  . '<label for="password">كلمة السر</label><input id="password" name="password" type="password" required autocomplete="current-password" dir="ltr" maxlength="200">'
  . '<button class="b p w" type="submit">دخول</button></form></main>';
ui_end();
