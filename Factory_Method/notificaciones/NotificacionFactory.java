package Factory_Method.notificaciones;

// NotificacionFactory.java
public abstract class NotificacionFactory {
    // Este es el "Factory Method"
    public abstract Notificacion crearNotificacion();

    public void enviarMensaje(String mensaje) {
        Notificacion n = crearNotificacion();
        n.enviar(mensaje);
    }
}