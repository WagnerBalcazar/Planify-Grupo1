package Factory_Method.notificaciones;

// Main.java
public class Main {
    public static void main(String[] args) {
        String miMensaje = "¡Hola! Este es un mensaje de prueba.";

        // Usando la fábrica de Email
        NotificacionFactory fabricaEmail = new EmailFactory();
        fabricaEmail.enviarMensaje(miMensaje);

        // Usando la fábrica de SMS
        NotificacionFactory fabricaSMS = new SMSFactory();
        fabricaSMS.enviarMensaje(miMensaje);
    }
}