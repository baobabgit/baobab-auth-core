Architecture Decision Records
=============================

Index des décisions d'architecture de ``baobab-auth-core``.

.. list-table::
   :header-rows: 1
   :widths: 12 60 12

   * - ADR
     - Titre
     - Statut
   * - :doc:`0001 <0001-architecture-hexagonale>`
     - Architecture hexagonale (domain / ports / testing)
     - Accepté
   * - :doc:`0002 <0002-value-objects-frozen-dataclass>`
     - Value objects en frozen dataclass
     - Accepté
   * - :doc:`0003 <0003-ports-typing-protocol>`
     - Ports en ``typing.Protocol`` runtime_checkable
     - Accepté
   * - :doc:`0004 <0004-fakes-dans-le-package>`
     - Fakes livrés dans le package (``testing/``)
     - Accepté
   * - :doc:`0005 <0005-librairie-metier-pure>`
     - Librairie métier pure, sans dépendance technique
     - Accepté
   * - :doc:`0006 <0006-tracabilite-specs-vs-backlog>`
     - Traçabilité : specs RST vs backlog Markdown
     - Accepté
   * - :doc:`0007 <0007-extension-token-provider-refresh>`
     - Extension du port ``TokenProvider`` (refresh tokens, révocation)
     - Accepté
   * - :doc:`0008 <0008-authcontext-minimal-en-0-2-0>`
     - ``AuthContext`` minimal en v0.2.0, complet en v0.3.0
     - Accepté
   * - :doc:`0009 <0009-rbac-authcontext-authorization-service>`
     - RBAC applicatif pur et ``AuthContext`` immutable
     - Accepté
   * - :doc:`0010 <0010-default-auth-catalog>`
     - Catalogue d'autorisation par défaut (``DefaultAuthCatalog``)
     - Accepté
   * - :doc:`0011 <0011-role-policy-super-admin>`
     - ``RolePolicy`` renforcée et règles strictes ``SUPER_ADMIN``
     - Accepté
   * - :doc:`0012 <0012-change-password-revoke-all-sessions>`
     - Création de ``ChangePassword`` et ``RevokeAllSessions``
     - Accepté
   * - :doc:`0013 <0013-error-codes-metier>`
     - Codes d'erreur métier sur les exceptions publiques
     - Accepté
   * - :doc:`0014 <0014-stabilisation-contrats-publics>`
     - Stabilisation des contrats publics, cas d'usage lecture/admin
     - Accepté

.. toctree::
   :maxdepth: 1
   :hidden:

   0001-architecture-hexagonale
   0002-value-objects-frozen-dataclass
   0003-ports-typing-protocol
   0004-fakes-dans-le-package
   0005-librairie-metier-pure
   0006-tracabilite-specs-vs-backlog
   0007-extension-token-provider-refresh
   0008-authcontext-minimal-en-0-2-0
   0009-rbac-authcontext-authorization-service
   0010-default-auth-catalog
   0011-role-policy-super-admin
   0012-change-password-revoke-all-sessions
   0013-error-codes-metier
   0014-stabilisation-contrats-publics
