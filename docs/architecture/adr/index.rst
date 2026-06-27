Architecture Decision Records
=============================

Index des décisions d'architecture de ``baobab-auth-core``.

================  ==================================================  ==========
ADR               Titre                                               Statut
================  ==================================================  ==========
:doc:`0001 <0001-architecture-hexagonale>`  Architecture hexagonale (domain / ports / testing)  Accepté
:doc:`0002 <0002-value-objects-frozen-dataclass>`  Value objects en frozen dataclass                   Accepté
:doc:`0003 <0003-ports-typing-protocol>`  Ports en ``typing.Protocol`` runtime_checkable      Accepté
:doc:`0004 <0004-fakes-dans-le-package>`  Fakes livrés dans le package (``testing/``)         Accepté
:doc:`0005 <0005-librairie-metier-pure>`  Librairie métier pure, sans dépendance technique    Accepté
================  ==================================================  ==========

.. toctree::
   :maxdepth: 1
   :hidden:

   0001-architecture-hexagonale
   0002-value-objects-frozen-dataclass
   0003-ports-typing-protocol
   0004-fakes-dans-le-package
   0005-librairie-metier-pure
