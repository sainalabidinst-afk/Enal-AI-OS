package com.enalai.os.android.domain.repository

import com.enalai.os.android.data.remote.dto.AuthResponse
import com.enalai.os.android.data.remote.dto.ChatRequest
import com.enalai.os.android.data.remote.dto.ChatResponse
import com.enalai.os.android.domain.model.AuthState

interface AuthRepository {
    suspend fun login(username: String, password: String): Result<AuthResponse>
    suspend fun saveSession(token: String)
    suspend fun clearSession()
    suspend fun currentAuth(): AuthState
}

interface ChatRepository {
    suspend fun sendMessage(request: ChatRequest): Result<ChatResponse>
}

interface ObservabilityRepository {
    suspend fun getLogs(): Result<Map<String, Any>>
    suspend fun getTraces(): Result<Map<String, Any>>
}
