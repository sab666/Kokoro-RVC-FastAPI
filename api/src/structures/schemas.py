from enum import Enum
from typing import List, Literal, Union

from pydantic import BaseModel, Field


class VoiceCombineRequest(BaseModel):
    """Request schema for voice combination endpoint that accepts either a string with + or a list"""

    voices: Union[str, List[str]] = Field(
        ...,
        description="Either a string with voices separated by + (e.g. 'voice1+voice2') or a list of voice names to combine",
    )


class TTSStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DELETED = "deleted"  # For files removed by cleanup


# OpenAI-compatible schemas
class WordTimestamp(BaseModel):
    """Word-level timestamp information"""
    word: str = Field(..., description="The word or token")
    start_time: float = Field(..., description="Start time in seconds")
    end_time: float = Field(..., description="End time in seconds")

class CaptionedSpeechResponse(BaseModel):
    """Response schema for captioned speech endpoint"""
    audio: bytes = Field(..., description="The generated audio data")
    words: List[WordTimestamp] = Field(..., description="Word-level timestamps")

class OpenAISpeechRequest(BaseModel):
    """Request schema for OpenAI-compatible speech endpoint"""
    model: str = Field(
        default="kokoro",
        description="The model to use for generation. Supported models: tts-1, tts-1-hd, kokoro"
    )
    input: str = Field(..., description="The text to generate audio for")
    voice: str = Field(
        default="af",
        description="The voice to use for generation. Can be a base voice or a combined voice name.",
    )
    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = Field(
        default="mp3",
        description="The format to return audio in. Supported formats: mp3, opus, flac, wav, pcm. PCM format returns raw 16-bit samples without headers. AAC is not currently supported.",
    )
    speed: float = Field(
        default=1.0,
        ge=0.25,
        le=4.0,
        description="The speed of the generated audio. Select a value from 0.25 to 4.0.",
    )
    stream: bool = Field(
        default=True,  # Default to streaming for OpenAI compatibility
        description="If true (default), audio will be streamed as it's generated. Each chunk will be a complete sentence.",
    )
    return_download_link: bool = Field(
        default=False,
        description="If true, returns a download link in X-Download-Path header after streaming completes",
    )

class CaptionedSpeechRequest(BaseModel):
    """Request schema for captioned speech endpoint"""
    model: str = Field(
        default="kokoro",
        description="The model to use for generation. Supported models: tts-1, tts-1-hd, kokoro"
    )
    input: str = Field(..., description="The text to generate audio for")
    voice: str = Field(
        default="af",
        description="The voice to use for generation. Can be a base voice or a combined voice name.",
    )
    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = Field(
        default="mp3",
        description="The format to return audio in. Supported formats: mp3, opus, flac, wav, pcm. PCM format returns raw 16-bit samples without headers. AAC is not currently supported.",
    )
    speed: float = Field(
        default=1.0,
        ge=0.25,
        le=4.0,
        description="The speed of the generated audio. Select a value from 0.25 to 4.0.",
    )
    return_timestamps: bool = Field(
        default=True,
        description="If true (default), returns word-level timestamps in the response",
    )
