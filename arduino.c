#include <Adafruit_NeoPixel.h>
#ifdef AVR
#include <avr/power.h>
#endif
#define PIN 9        // Hier wird angegeben, an welchem digitalen Pin die WS2812 LEDs bzw. NeoPixel angeschlossen sind
#define NUMPIXELS 8  // Hier wird die Anzahl der angeschlossenen WS2812 LEDs bzw. NeoPixel angegeben
#define BUTTON_PIN 6
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

bool blinking = true;
int pause = 100;  // 100 Millisekunden Pause bis zur Ansteuerung der nächsten LED.
int buttonState;
int lastButtonState = LOW;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // Set the button pin as an input with internal pullup resistor
  pixels.begin();
}

void loop() {
  buttonState = digitalRead(BUTTON_PIN);  // Read the button state

  if (buttonState != lastButtonState) {  // Check if the button state has changed
    if (buttonState == LOW) {            // If the button is pressed
      blinking = !blinking;              // Toggle the blinking state
    }
    delay(50);  // Debounce delay
  }
  lastButtonState = buttonState;  // Update the last button state

  if (blinking) {                                      // Only blink the neopixels if the blinking state is tru
    pixels.setPixelColor(1, pixels.Color(0, 255, 0));  // Pixel1 leuchtet in der Farbe Grün
    pixels.show();                                     // Durchführen der Pixel-Ansteuerung
    delay(pause);                                      // Pause, in dieser Zeit wird nichts verändert.
    pixels.setPixelColor(2, pixels.Color(0, 150, 0));  // Pixel2 leuchtet in der Farbe Grün
    pixels.show();                                     // Durchführen der Pixel-Ansteuerung
    delay(pause);                                      // Pause, in dieser Zeit wird nichts verändert.
    pixels.setPixelColor(3, pixels.Color(0, 50, 0));   // Pixel3 leuchtet in der Farbe Grün
    pixels.show();                                     // Durchführen der Pixel-Ansteuerung
    delay(pause);                                      // Pause, in dieser Zeit wird nichts verändert.
    pixels.setPixelColor(4, pixels.Color(0, 10, 0));   // Pixel4 leuchtet in der Farbe Grün
    pixels.show();                                     // Durchführen der Pixel-Ansteuerung
    delay(pause);                                      // Pause, in dieser Zeit wird nichts verändert.
    pixels.setPixelColor(5, pixels.Color(0, 1, 0));    // Pixel5 leuchtet in der Farbe Grün
    pixels.show();                                     // Durchführen der Pixel-Ansteuerung
    delay(pause);                                      // Pause, in dieser Zeit wird nichts verändert.

    // Zurücksetzen aller Pixelfarben auf Stufe "0" (aus)
    pixels.setPixelColor(1, pixels.Color(0, 0, 0));
    pixels.setPixelColor(2, pixels.Color(0, 0, 0));
    pixels.setPixelColor(3, pixels.Color(0, 0, 0));
    pixels.setPixelColor(4, pixels.Color(0, 0, 0));
    pixels.setPixelColor(5, pixels.Color(0, 0, 0));
    pixels.show();  // Durchführen der Pixel-Ansteuerung
    delay(pause);   // Pause, die LEDs bleiben in dieser Zeit aus
  } else {
    // Turn off all neopixels if the blinking state is false
    for (int i = 0; i < NUMPIXELS; i++) {
      pixels.setPixelColor(i, pixels.Color(0, 0, 0));
    }
    pixels.show();
  }
}