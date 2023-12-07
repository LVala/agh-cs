#include "wavetable.h"

float saw_wavetable[WAVETABLE_LEN];
float sine_wavetable[WAVETABLE_LEN];
static uint8_t wavetables_initialized = 0;

float CHROMATIC_BASE = pow(2.0f, 1.0f / 12.0f);

static float PitchToFreq(uint8_t pitch_midi) {
  return 440*pow(CHROMATIC_BASE, (float)pitch_midi - 69);
}

static void SineWavetableInit() {
  float d_phase = (2.0f * (float)M_PI) / WAVETABLE_LEN;
  float phase = 0;
  for (uint16_t i = 0; i < WAVETABLE_LEN; i++) {
    sine_wavetable[i] = sin(phase);
    phase += d_phase;
  }
}

static void SawWavetableInit() {
  float octaves = (int)(SAMPLE_RATE / 2.0 / 440.0);
  for(int octave = 1; octave < octaves; octave++) {
    float d_phase = (octave * 2.0f * (float)M_PI) / WAVETABLE_LEN;
    float phase = 0;
    float sign = (octave & 1) ? -1.0f : 1.0f;
    for (uint16_t i = 0; i < WAVETABLE_LEN; i++) {
      saw_wavetable[i] += (sign * sin(phase) / octave) * (2.0f / (float)M_PI);
      phase += d_phase;
    }
  }
}

void Wavetable_Init(Wavetable_State *state, uint8_t wave) {
  if (!wavetables_initialized) {
    SineWavetableInit();
    SawWavetableInit();
  }

  state->wave = wave;
  state->phase = 0;
  state->pitch_midi = 0;
  state->pitch_hz = 0;
  state->d_phase = (state->pitch_hz/SAMPLE_RATE) * WAVETABLE_LEN;

  ADSR_Init(&state->adsr_state, DEFAULT_ATTACK, DEFAULT_DECAY, DEFAULT_SUSTAIN, DEFAULT_RELEASE, DEFAULT_SCALE);
}

void Wavetable_NoteOn(Wavetable_State *state, uint8_t pitch_midi) {
  state->phase = 0;
  state->pitch_midi = pitch_midi;
  state->pitch_hz = PitchToFreq(pitch_midi);
  state->d_phase = (state->pitch_hz/SAMPLE_RATE) * WAVETABLE_LEN;
}

void Wavetable_NoteOff(Wavetable_State *state, uint8_t pitch_midi) {
  if (state->pitch_midi == pitch_midi) {
    state->phase = 0;
    state->pitch_midi = 0;
    state->pitch_hz = 0;
    state->d_phase = (state->pitch_hz/SAMPLE_RATE) * WAVETABLE_LEN;
  }
}

void Wavetable_GetSamples(Wavetable_State *state, float *buffer, int num_frames) {
  float sample;
  for (uint32_t i = 0; i<num_frames; i++) {
    sample = sine_wavetable[(uint32_t)state->phase];
    buffer[2*i] = sample;
    buffer[2*i+1] = sample;
    state->phase += state->d_phase;
    if (state->phase > WAVETABLE_LEN) {
      state->phase -= WAVETABLE_LEN;
    }
  }
}
