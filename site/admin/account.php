<?php
require __DIR__ . '/../inc/bootstrap.php';
require __DIR__ . '/_ui.php';
$u = require_login();
$err = ''; $ok = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  csrf_check();
  $cur = isset($_POST['current']) ? (string)$_POST['current'] : '';
  $new = isset($_POST['new']) ? (string)$_POST['new'] : '';
  $new2 = isset($_POST['new2']) ? (string)$_POST['new2'] : '';
  $email = strtolower(trim(isset($_POST['email']) ? (string)$_POST['email'] : ''));
  $st = db()->prepare('SELECT password_hash FROM pc_users WHERE id = ?'); $st->execute(array($u['id'])); $row = $st->fetch();
  if (!$row || !password_verify($cur, $row['password_hash'])) { $err = 'كلمة السر الحالية غير صحيحة.'; }
  elseif (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 190) { $err = 'البريد الإلكتروني غير صالح.'; }
  elseif ($new !== '' && ($new !== $new2 || !pw_ok_policy($new))) { $err = 'كلمة السر الجديدة يجب أن تكون 12 حرفاً على الأقل ومتطابقة.'; }
  else {
    $dup = db()->prepare('SELECT id FROM pc_users WHERE email = ? AND id <> ?'); $dup->execute(array($email, $u['id']));
    if ($dup->fetch()) { $err = 'هذا البريد مستعمل من حساب آخر.'; }
    else {
      if ($new !== '') db()->prepare('UPDATE pc_users SET email = ?, password_hash = ? WHERE id = ?')->execute(array($email, hash_pw($new), $u['id']));
      else db()->prepare('UPDATE pc_users SET email = ? WHERE id = ?')->execute(array($email, $u['id']));
      session_regenerate_id(true);
      header('Location: account.php?m=pwd'); exit;
    }
  }
  $u['email'] = $email ?: $u['email'];
}
ui_head('حسابي', 'ad');
echo '<div class="app">'; ui_side($u, 'acc'); echo '<main>' . ui_flash() . '<h1>حسابي</h1>' . ($err ? '<div class="al bad" role="alert">' . e($err) . '</div>' : '')
  . '<form method="post" class="cd fm" autocomplete="off">' . csrf_field()
  . '<label for="email">البريد الإلكتروني</label><input id="email" name="email" type="email" required value="' . e($u['email']) . '" dir="ltr" maxlength="190">'
  . '<label for="new">كلمة سر جديدة (اتركها فارغة إن لم ترد تغييرها)</label><input id="new" name="new" type="password" autocomplete="new-password" dir="ltr" maxlength="200"><span class="hint">12 حرفاً على الأقل. يُفضّل جملة طويلة يسهل تذكّرها.</span>'
  . '<label for="new2">تأكيد كلمة السر الجديدة</label><input id="new2" name="new2" type="password" autocomplete="new-password" dir="ltr" maxlength="200">'
  . '<label for="current">كلمة السر الحالية (مطلوبة للتأكيد)</label><input id="current" name="current" type="password" required autocomplete="current-password" dir="ltr" maxlength="200">'
  . '<p><button class="b p" type="submit">حفظ التغييرات</button></p></form></main></div>';
ui_end();
