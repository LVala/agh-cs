#ifndef INC_ADSR_H_
#define INC_ADSR_H_

#include <stdint.h>

typedef struct {
  float attack; // attack duration (amplitude 0 -> max) [s]
  float decay; // decay duration (amplitude max -> sustain level) [s]
  float sustain; // sustain level (for example 70% of max amplitude) [%]
  float release; // release time (amplitude sustain level -> 0) [s]

  float scale;
  float max_amplitude;
  float start_time; // current start time
  float release_time; // current release time
  float cur_amplitude;
  float release_amplitude;
} ADSR_State;

#define DEFAULT_ATTACK    0.1
#define DEFAULT_DECAY     0.05
#define DEFAULT_SUSTAIN   0.8
#define DEFAULT_RELEASE   0.1
#define DEFAULT_SCALE     1.0

void ADSR_Init(ADSR_State *self, float attack, float decay, float sustain, float release, float scale);
void ADSR_Reset(ADSR_State *self);
void ADSR_NoteOn(ADSR_State *self, int8_t velocity, float time);
void ADSR_NoteOff(ADSR_State *self, float time);
void ADSR_GetSamples(ADSR_State *self, float *inout_samples, int frame_count, float time);
int8_t ADSR_Active(ADSR_State *self, float time);
int8_t ADSR_Releasing(ADSR_State *self, float time);

#endif
