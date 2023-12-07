#ifndef __MIDI_H
#define __MIDI_H

#include "usb_host.h"
#include "synth.h"
#include "../../Drivers/USBH_midi_class/Inc/usbh_MIDI.h"

void Midi_Start(void);
void Midi_Stop(void);

#endif
