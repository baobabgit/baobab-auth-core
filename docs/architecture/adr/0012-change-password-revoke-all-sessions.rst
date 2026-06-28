ADR-0012 — Création de ``ChangePassword`` et ``RevokeAllSessions`` en v0.4.0
==========================================================================

:Statut: Accepté
:Date: 2026-06-28
:Version: v0.4.0
:Backlogs: BL-040-013, BL-040-014

Contexte
--------

Le cahier des charges v0.4.0 liste en **préconditions** (§2) ``ChangePassword``,
``RevokeAllSessions`` et ``LockoutPolicy`` comme « devant être fonctionnels ».
Après inventaire, ``ChangePassword`` et ``RevokeAllSessions`` **n'existent pas**
dans le code : ils n'étaient pas dans le périmètre des versions 0.2.0 ni 0.3.0.
En revanche, le cahier les **spécifie** au §12 (durcissements) et exige leurs
tests au §13.

Décision
--------

Traiter cette incohérence sans intervention bloquante : **créer** ``ChangePassword``
et ``RevokeAllSessions`` dans le périmètre v0.4.0 (backlogs ajoutés BL-040-013 et
BL-040-014), en respectant les règles du §12 :

- ``ChangePassword`` : vérification de l'ancien mot de passe, validation du nouveau
  (``PasswordPolicy``), nouveau ≠ ancien, hachage via le port, révocation des
  autres sessions selon ``SessionPolicy.revoke_other_sessions_on_password_change``,
  audit ``PASSWORD_CHANGED`` sans secret.
- ``RevokeAllSessions`` : un utilisateur révoque ses propres sessions ; un ``ADMIN``
  révoque les sessions d'un compte standard ; un ``SUPER_ADMIN`` ne peut être
  neutralisé abusivement par un acteur de rang inférieur ; audit
  ``ALL_SESSIONS_REVOKED`` avec ``count``.

``LockoutPolicy`` correspond aux paramètres de lockout déjà portés par
``SessionPolicy`` ; ``AuthenticateUser`` (v0.2.0) implémente déjà le lockout.

Conséquences
------------

- Ajout rétrocompatible (MINOR) de deux cas d'usage applicatifs.
- L'incohérence des préconditions est tracée ici plutôt que bloquante.
