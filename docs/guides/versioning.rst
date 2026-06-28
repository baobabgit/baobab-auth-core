Versionnage et compatibilité (v0.5.0)
=====================================

``baobab-auth-core`` suit le **Semantic Versioning** (sans borne supérieure).

- **MAJOR** : rupture d'un contrat public (suppression / modification incompatible
  d'un symbole de ``__all__``, d'une signature de port, d'un ``error_code`` ou du
  mapping ``DefaultAuthCatalog``). Accompagné d'une entrée ``CHANGELOG`` *BREAKING*
  et d'une note de migration.
- **MINOR** : ajout rétrocompatible (nouveau cas d'usage, nouveau champ optionnel,
  nouvelle exception, méthode additive sur un port).
- **PATCH** : correction rétrocompatible (y compris republication packaging, cf.
  v0.4.1).

Surface du contrat
------------------

Le contrat est constitué de ``baobab_auth_core.__all__``, des signatures des ports
(``typing.Protocol``), de la hiérarchie d'exceptions (avec ``error_code``) et du
catalogue ``DefaultAuthCatalog``. La compatibilité inter-briques se valide par
git-ref sur ``version/vX.Y.Z`` (voir :doc:`how-to/integration-validation`).
