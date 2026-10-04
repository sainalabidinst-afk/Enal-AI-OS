package com.enalai.os.android.domain.model

data class ChatMessage(
    val id: String,
    val role: String,
    val content: String,
    val timestamp: String
)

data class Trace(
    val id: String,
    val timestamp: String,
    val service: String,
    val durationMs: Long,
    val status: String
)

data class LogEntry(
    val id: String,
    val timestamp: String,
    val level: String,
    val message: String
)

data class AuthState(
    val token: String? = null,
    val isAuthenticated: Boolean = false
)
