===================
Crumges Autogestión
===================

Acceso a Crumges Autogestión desde el Odoo de cada cliente, para que el cliente se autogestione
(hoy: ambientes, respaldos y estado del servidor; más adelante, por ejemplo, tickets o seguimiento de proyectos).

* Ícono en la barra superior con el estado del servidor (recursos, instancias, último respaldo y avisos)
  y un botón para abrir el panel.
* Opción «Autogestión» en el menú del usuario.
* Quita del menú del usuario: Soporte, Mi cuenta de Odoo.com e Instalar aplicación (para todos).

Configuración
=============

1. Dar el permiso **Autogestión / Usuario** a quienes se autogestionan (Ajustes › Usuarios).
2. En Ajustes › Generales › Crumges Autogestión, revisar la dirección del panel (por defecto ``/autogestion/``).

El estado en vivo requiere que Autogestión esté en el mismo dominio que el Odoo (por ejemplo
``cliente.com/odoo`` y ``cliente.com/autogestion``). Si no lo está, desactivar «Mostrar estado del
servidor»: el ícono queda como acceso directo.
