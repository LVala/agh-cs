#include "synth.h"

static void UpdateAudioBuffer(uint32_t start_frame, uint32_t num_frames);

uint16_t audio_buffer[AUDIO_BUFFER_SAMPLES];
float sample_N;

uint16_t base = 16000;
uint16_t scaled_base = 16000 / POLY_MAX;

Wavetable_State wavetables[POLY_MAX];

float synth_time = 0.0; // synthesizer clock for adsr

void Synth_Init() {
  for(int note = 0; note<POLY_MAX; note++) {
    Wavetable_Init(&wavetables[note], WAVE_SINE);
  }
  UpdateAudioBuffer(0, AUDIO_BUFFER_FRAMES);
}

uint8_t Synth_Play() {
  return HAL_I2S_Transmit_DMA(&hi2s3, audio_buffer, AUDIO_BUFFER_SAMPLES);
}

void Synth_NoteOn(uint8_t midi_param0, uint8_t midi_param1) {
  for (int8_t i=0; i<POLY_MAX; i++) {
    if (ADSR_Active(&(&wavetables[i])->adsr_state, synth_time) == 0) {
	  // activete the note
      Wavetable_NoteOn(&wavetables[i], midi_param0);
      ADSR_NoteOn(&(&wavetables[i])->adsr_state, 127.0, synth_time);
      break;
	}
  }
}

void Synth_NoteOff(uint8_t midi_param0, uint8_t midi_param1) {
  for (int8_t i=0; i<POLY_MAX; i++) {
    if (wavetables[i].pitch_midi == midi_param0) {
      if (ADSR_Releasing(&(&wavetables[i])->adsr_state, synth_time) == 1) {
        // note already releasing
    	continue;
      }
      ADSR_NoteOff(&(&wavetables[i])->adsr_state, synth_time);
      break;
    }
  }
}

static void UpdateAudioBuffer(uint32_t start_frame, uint32_t end_frame) {
  // start_frame is inclusive, end_frame exclusive
  float buffer[AUDIO_BUFFER_SAMPLES];
  for(int i = 0; i<AUDIO_BUFFER_SAMPLES; i++) {buffer[i] = 0;}
  float _buffer[AUDIO_BUFFER_SAMPLES];
  for(int i = 0; i<AUDIO_BUFFER_SAMPLES; i++) {_buffer[i] = 0;}

  for(int note = 0; note < POLY_MAX; note++) {
    Wavetable_GetSamples(&wavetables[note], _buffer, end_frame - start_frame);
    ADSR_GetSamples(&(&wavetables[note])->adsr_state, _buffer, end_frame - start_frame, synth_time);

    for(int i = 0; i < end_frame - start_frame; i++) {
      buffer[2*i] += _buffer[2*i];
      buffer[2*i+1] += _buffer[2*i+1];
    }
  }

  uint32_t i = 0;
  for (uint32_t frame = start_frame; frame < end_frame; frame++) {
    float scaled = buffer[2*i] * scaled_base;
    uint16_t value = (uint16_t)(base + scaled);

    audio_buffer[2*frame] = value;
    audio_buffer[2*frame+1] = value;
    i++;
  }
}

void HAL_I2S_TxHalfCpltCallback(I2S_HandleTypeDef *hi2s) {
  UpdateAudioBuffer(0, AUDIO_BUFFER_FRAMES/2);
  synth_time += (float)(AUDIO_BUFFER_FRAMES/2)/SAMPLE_RATE;
}

void HAL_I2S_TxCpltCallback(I2S_HandleTypeDef *hi2s) {
  UpdateAudioBuffer(AUDIO_BUFFER_FRAMES/2, AUDIO_BUFFER_FRAMES);
  synth_time += (float)(AUDIO_BUFFER_FRAMES/2)/SAMPLE_RATE;
}
