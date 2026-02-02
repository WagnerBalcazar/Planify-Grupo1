package Factory_Method.notificaciones;

// EmailFactory.java
public class EmailFactory extends NotificacionFactory {
    @Override
    public Notificacion crearNotificacion() {
        return new EmailNotificacion();
    }
}