====================
Journal Account Sync
====================

Este módulo extiende la funcionalidad base de Odoo para mantener la consistencia entre el nombre de los diarios de liquidez y sus cuentas contables asociadas.

Casos de Uso
============
* Cuando el usuario renombra un diario de Banco o Efectivo desde la vista de configuración.
* Evita la discrepancia visual y contable donde un diario tiene un nombre y su cuenta subyacente mantiene el nombre original.

Modo de Uso
===========
1. Ve a **Contabilidad > Configuración > Diarios**.
2. Selecciona un diario de tipo Banco o Efectivo.
3. Cambia el nombre del diario.
4. Automáticamente, la cuenta contable predeterminada de ese diario cambiará su nombre para coincidir de forma exacta.

Créditos
========

Autor
-----
* Crumges

Colaboradores
-------------
* Crumges <https://crumges.com>
