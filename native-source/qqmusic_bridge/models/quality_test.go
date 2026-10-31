package models

import "testing"

func TestAudioQualityFileMapping(t *testing.T) {
	tests := []struct {
		quality AudioQuality
		prefix  string
		ext     string
	}{
		{QualityStandard, "C400", "m4a"},
		{QualityHQ, "M800", "mp3"},
		{QualitySQ, "F000", "flac"},
		{QualityHiRes, "RS01", "flac"},
		{AudioQuality("unknown"), "C400", "m4a"},
	}
	for _, tt := range tests {
		if got := tt.quality.GetFilePrefix(); got != tt.prefix {
			t.Errorf("%q prefix = %q, want %q", tt.quality, got, tt.prefix)
		}
		if got := tt.quality.GetFileExt(); got != tt.ext {
			t.Errorf("%q extension = %q, want %q", tt.quality, got, tt.ext)
		}
	}
}
