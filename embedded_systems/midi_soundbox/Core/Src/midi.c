#include "midi.h"

#define RX_BUFF_SIZE 64

extern USBH_HandleTypeDef hUsbHostFS;
uint8_t MIDI_RX_Buffer[RX_BUFF_SIZE];

static void HandleMidi(uint8_t midi_cmd, uint8_t midi_param0, uint8_t midi_param1);

void Midi_Start(void) {
  USBH_MIDI_Receive(&hUsbHostFS, MIDI_RX_Buffer, RX_BUFF_SIZE);
}

void Midi_Stop(void) {
  USBH_MIDI_Stop(&hUsbHostFS);
}

void USBH_MIDI_ReceiveCallback(USBH_HandleTypeDef *phost) {
  // each USB midi package is 4 bytes long
  uint16_t numberOfPackets = USBH_MIDI_GetLastReceivedDataSize(&hUsbHostFS) / 4;

  for(uint16_t i = 0; i < numberOfPackets; ++i) {
    uint8_t cin_cable   = MIDI_RX_Buffer[4*i+0];
    uint8_t midi_cmd    = MIDI_RX_Buffer[4*i+1];
    uint8_t midi_param0 = MIDI_RX_Buffer[4*i+2];
    uint8_t midi_param1 = MIDI_RX_Buffer[4*i+3];
    if(cin_cable == 0 || cin_cable == 11) {
      continue;
    }
    HandleMidi(midi_cmd, midi_param0, midi_param1);
  }

  USBH_MIDI_Receive(&hUsbHostFS, MIDI_RX_Buffer, RX_BUFF_SIZE);
}

static void HandleMidi(uint8_t midi_cmd, uint8_t midi_param0, uint8_t midi_param1) {
  switch (midi_cmd & 0xf0) {
  case 0x80:
	Synth_NoteOff(midi_param0, midi_param1);
	break;
  case 0x90:
	Synth_NoteOn(midi_param0, midi_param1);
	break;
  }
}
