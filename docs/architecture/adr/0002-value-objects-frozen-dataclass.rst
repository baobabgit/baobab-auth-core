ADR-0002 — Value objects en frozen dataclass, entités en dataclass mutable
==========================================================================

:Statut: Accepté
:Date: 2026-06-26
:Contexte version: v0.1.0
:Spec: FEAT-010.2, FEAT-010.3

Contexte
--------

Le domaine distingue deux natures d'objets : les **value objects** (identité par
valeur, ex. ``Email``, ``PermissionName``) et les **entités** (identité propre et
cycle de vie, ex. ``User``, ``Session``). Il faut un mécanisme uniforme,
fortement typé, qui exprime cette distinction et applique les invariants.

Décision
--------

* Les **value objects** sont des ``@dataclass(frozen=True)`` : immuables,
  comparables par valeur, hashables. La normalisation et la validation ont lieu
  dans ``__post_init__`` (ex. ``Email`` en minuscules ; rejet si invalide).
* Les **entités** sont des ``@dataclass`` mutables : elles portent un identifiant
  et exposent des méthodes métier qui font évoluer leur état (ex.
  ``User.lock()``). Les invariants de construction sont vérifiés dans
  ``__post_init__``.
* ``AuditEvent`` est une **exception** : entité immuable (``frozen=True``) car un
  événement d'audit ne doit jamais être modifié après émission.

Conséquences
------------

**Positives**

* Immutabilité des value objects → sûreté (pas d'effet de bord, hashables comme
  clés).
* La mutation d'un frozen lève ``FrozenInstanceError``, testable explicitement.
* Validation centralisée à la construction : un objet existant est toujours valide.

**Négatives / coûts**

* Modifier un value object impose d'en recréer un nouveau.
* ``__post_init__`` sur frozen nécessite ``object.__setattr__`` pour la
  normalisation interne.

Alternatives écartées
---------------------

* **Classes Pydantic pour le domaine** : rejetées pour ne pas imposer Pydantic au
  cœur métier (réservé à la config via ``pydantic-settings``).
* **``NamedTuple``** : insuffisant pour la validation et le masquage des secrets.
