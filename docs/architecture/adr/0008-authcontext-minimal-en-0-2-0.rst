ADR-0008 — ``AuthContext`` minimal en v0.2.0, complet en v0.3.0
==============================================================

:Statut: Accepté
:Date: 2026-06-28
:Version: v0.2.0
:Backlogs: BL-020-006

Contexte
--------

Le cahier des charges v0.2.0 référence ``AuthContext`` dans la commande
``RevokeSessionCommand`` (``actor: AuthContext | None``) tout en précisant que,
« si ``AuthContext`` n'est pas encore complet, accepter une forme minimale ou
reporter les contrôles avancés à 0.3.0 ». ``AuthContext`` est entièrement
spécifié dans le cahier v0.3.0 (RBAC, rôles, permissions agrégées).

Décision
--------

En v0.2.0 :

- ``RevokeSessionCommand`` accepte un **acteur minimal** sous la forme
  ``actor_subject: AuthSubject | None`` plutôt qu'un ``AuthContext`` complet.
- ``RevokeSession`` révoque une session existante de façon idempotente et produit
  ``SESSION_REVOKED`` ; les contrôles d'autorisation fins (vérification de rôle /
  permission de l'acteur) sont **reportés à v0.3.0**.

Conséquences
------------

- Évite d'introduire prématurément un ``AuthContext`` partiel qui devrait changer
  en v0.3.0 (rupture de contrat évitée).
- La v0.3.0 introduira ``AuthContext`` complet et durcira ``RevokeSession`` /
  ``AssignRole`` / ``RemoveRole`` avec les contrôles d'autorisation.
- Aucun token brut n'est audité, conformément aux règles de sécurité.
