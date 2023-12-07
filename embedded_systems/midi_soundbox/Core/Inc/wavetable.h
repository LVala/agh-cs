#ifndef __WAVETABLE_H
#define __WAVETABLE_H


#include <math.h>
#include <stdint.h>
#include "adsr.h"

#define SAMPLE_RATE 48000
#define WAVETABLE_LEN 4048
#define WAVE_SINE 0
#define WAVE_SAW 1

typedef struct {
  uint8_t wave;
  float phase;
  float d_phase;
  int8_t pitch_midi;
  float pitch_hz;
  ADSR_State adsr_state;
} Wavetable_State;

void Wavetable_Init(Wavetable_State *state, uint8_t wave);
void Wavetable_NoteOn(Wavetable_State *state, uint8_t pitch_midi);
void Wavetable_NoteOff(Wavetable_State *state, uint8_t pitch_midi);
void Wavetable_GetSamples(Wavetable_State *state, float *buffer, int num_frames);


#endif
