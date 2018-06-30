import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalInput;
import com.pi4j.io.gpio.GpioPinDigitalOutput;
import com.pi4j.io.gpio.PinPullResistance;
import com.pi4j.io.gpio.RaspiPin;
import com.pi4j.io.gpio.event.GpioPinDigitalStateChangeEvent;
import com.pi4j.io.gpio.event.GpioPinListenerDigital;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class RoboClient {

   static class RobotState {

      final long change_delay = 0; // do not change command in 500 ms
      long last_command;

      final char off   = 46;
      final char fwr   = 94;
      final char lft   = 60;
      final char rgt   = 62;
      char state;

      public RobotState()
      {
         state = off;
         last_command = System.currentTimeMillis();
      }

      public char getState() { return state; }

      public void goLeft()    {
         if (state == off && (System.currentTimeMillis() - last_command) > change_delay)
         {
            state = lft;
            last_command = System.currentTimeMillis();
         }
      }
      public void goRight()   {
        if (state == off && (System.currentTimeMillis() - last_command) > change_delay)
        {
           System.out.println("GO RIGHT");
           state = rgt;
           last_command = System.currentTimeMillis();
        }
      }
      public void goForward() {
         if (state == off && (System.currentTimeMillis() - last_command) > change_delay)
         {
            state = fwr;
            last_command = System.currentTimeMillis();
         }
      }

      public void stopLeft()  {
         if (state == lft && (System.currentTimeMillis() - last_command) > change_delay)
         {
            state = off;
            last_command = System.currentTimeMillis();
         }
      }
      public void stopRight() {
         if (state == rgt && (System.currentTimeMillis() - last_command) > change_delay)
         {
            System.out.println("STOP RIGHT");
            state = off;
            last_command = System.currentTimeMillis();
         }
      }
      public void stopForward() {
         if (state == fwr && (System.currentTimeMillis() - last_command) > change_delay)
         {
            state = off;
            last_command = System.currentTimeMillis();
         }
      }

      public String toString() { return String.valueOf(state); }
   }

   public static void main(String[] args) throws InterruptedException {

      final GpioController gpio                 = GpioFactory.getInstance();

      // hardware GPIO13, GPIO19, GPIO26 (from T extension pinout)
      final GpioPinDigitalInput myButtonLeft    = gpio.provisionDigitalInputPin(RaspiPin.GPIO_23, PinPullResistance.PULL_DOWN);
      final GpioPinDigitalInput myButtonForward = gpio.provisionDigitalInputPin(RaspiPin.GPIO_24, PinPullResistance.PULL_DOWN);
      final GpioPinDigitalInput myButtonRight   = gpio.provisionDigitalInputPin(RaspiPin.GPIO_25, PinPullResistance.PULL_DOWN);

      final RobotState state = new RoboClient.RobotState();


      myButtonForward.addListener(new GpioPinListenerDigital() {
         @Override
         public void handleGpioPinDigitalStateChangeEvent(GpioPinDigitalStateChangeEvent event) {
            if(event.getState().isHigh())
            {
               // go forward if no other state is on
               state.goForward();
System.out.println("FORW!!!");
            }
            else
            {
               // on forward release, turn off
               state.stopForward();
            }
         }
      });

      myButtonLeft.addListener(new GpioPinListenerDigital() {
         @Override
         public void handleGpioPinDigitalStateChangeEvent(GpioPinDigitalStateChangeEvent event) {
            if(event.getState().isHigh())
            {
               // only turn left if no other state is on
               state.goLeft();
System.out.println("LEFT!!!");
            }
            else
            {
               // on left release, turn off
               state.stopLeft();
            }
         }
      });

      myButtonRight.addListener(new GpioPinListenerDigital() {
         @Override
         public void handleGpioPinDigitalStateChangeEvent(GpioPinDigitalStateChangeEvent event) {
            if(event.getState().isHigh())
            {
               // only turn right if no other state is on
               state.goRight();
            }
            else
            {
               // on right release, turn off
               state.stopRight();
            }
         }
      });

      while(true)
      {
         Thread.sleep(500);

         System.out.println(state);

         try
         {
            // TODO: dont sent stop and let client stop if dont reveice other commands
            Process p = Runtime.getRuntime().exec("rpi-rf_send "+state.getState());
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            //int ret = new Integer(in.readLine()).intValue();
            //System.out.println("value is : "+ret);
System.out.println(in.readLine());
         }
         catch(Exception e)
         {
            e.printStackTrace();
            System.out.println(e.getMessage());
         }

      }
   }
}
