package Factory_Method.notificaciones;

// SMSFactory.java
public class SMSFactory extends NotificacionFactory {
    @Override
    public Notificacion crearNotificacion() {
        return new SMSNotificacion();
    }
}