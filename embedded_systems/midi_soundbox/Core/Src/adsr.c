#include "adsr.h"

static float get_sample(ADSR_State *self, float time);

void ADSR_Init(ADSR_State *self, float attack, float decay, float sustain, float release, float scale) {
  self->attack  = attack;
  self->decay   = decay;
  self->sustain = sustain;
  self->release = release;
  self->scale   = scale;
  ADSR_Reset(self);
}

void ADSR_Reset(ADSR_State *self) {
  self->max_amplitude = -1;
  self->cur_amplitude = -1;
  self->start_time = -1;
  self->release_time = -1;
  self->release_amplitude = -1;
}

void ADSR_NoteOn(ADSR_State *self, int8_t velocity, float time) {
  self->max_amplitude = self->scale * (float)velocity/127.0;
  self->start_time = time;
  self->release_time = -1;
  self->cur_amplitude = 0;
  self->release_amplitude = 0;
}

void ADSR_NoteOff(ADSR_State *self, float time) {
  if(self->release_time > 0) {
    return;
  }
  self->release_time = time;
  self->release_amplitude = self->cur_amplitude;
}

void ADSR_GetSamples(ADSR_State *self, float *inout_samples, int frame_count, float time)
{
  float cur_time = time;
  for(int frame = 0; frame < frame_count; frame++) {
    float sample_f = get_sample(self, cur_time);
    inout_samples[2*frame]   *= sample_f;
    inout_samples[2*frame+1] *= sample_f;
    cur_time = time + (float)frame/48000; //SAMPLE RATE (or FRAME RATE)
  }
}

// TEST_MODE sets amplitude = 1.0 when active.
#define TEST_MODE 1

static float get_sample(ADSR_State *self, float time)
{
  if( self->start_time < 0) {
    // reset state
    return 0;
  }
  if (self->release_time < self->start_time) {
    // Attack, Decay, Sustain
    float cur_time = time - self->start_time;
    if (cur_time <= self->attack) {
      // Attack
      self->cur_amplitude = cur_time / self->attack;
#if TEST_MODE == 1
      return 1.0;
#else
      return self->cur_amplitude * self->max_amplitude;
#endif
    }
    cur_time -= self->attack;
    if (cur_time <= self->decay) {
      // Decay
      self->cur_amplitude =
          self->sustain + (1.0f - self->sustain) * (1.0f - cur_time / self->decay);
#if TEST_MODE == 1
      return 1.0;
#else
      return self->cur_amplitude * self->max_amplitude;
#endif
    }
    // Sustain
    self->cur_amplitude = self->sustain;
#if TEST_MODE == 1
    return 1.0;
#else
    return self->cur_amplitude * self->max_amplitude;
#endif
  }
  else {
    float cur_time = time - self->release_time;
    if (cur_time <= self->release) {
      // Release
#if TEST_MODE == 1
      return 1.0;
#else
      return self->release_amplitude * (1.0f - cur_time / self->release) * self->max_amplitude;
#endif
    }
    // done
    self->cur_amplitude = 0.0f;
    return self->cur_amplitude;
  }
}

int8_t ADSR_Active(ADSR_State *self, float time) {
  if (self->start_time < 0.0) {
    return 0;
  }
  else if (time >= self->start_time) {
    if (self->release_time < 0.0) {
      return 1; // prior to noteOff
    }
    else if (time - self->release_time <= self->release) {
      return 1; // during release
    }
    else {
      return 0; // after release
    }
  }
  // time prior to startTime?
  return 0;
}

int8_t ADSR_Releasing(ADSR_State *self, float time) {
  return self->release_time > 0;
}
