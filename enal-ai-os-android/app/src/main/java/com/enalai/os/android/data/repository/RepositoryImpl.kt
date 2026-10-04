package com.enalai.os.android.data.repository

import com.enalai.os.android.data.local.SessionStore
import com.enalai.os.android.data.remote.EnalApi
import com.enalai.os.android.data.remote.dto.AuthResponse
import com.enalai.os.android.data.remote.dto.ChatRequest
import com.enalai.os.android.data.remote.dto.ChatResponse
import com.enalai.os.android.domain.model.AuthState
import com.enalai.os.android.domain.repository.AuthRepository
import com.enalai.os.android.domain.repository.ChatRepository
import com.enalai.os.android.domain.repository.ObservabilityRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class AuthRepositoryImpl(private val api: EnalApi, private val sessionStore: SessionStore) : AuthRepository {
    override suspend fun login(username: String, password: String) = runCatching {
        val response = api.login(mapOf("username" to username, "password" to password))
        if (response.isSuccessful) response.body() ?: throw IllegalStateException("Empty auth body") else throw IllegalStateException(response.errorBody()?.string())
    }

    override suspend fun saveSession(token: String) = sessionStore.save(token)
    override suspend fun clearSession() = sessionStore.clear()
    override suspend fun currentAuth(): AuthState = sessionStore.token.map { token -> AuthState(token = token, isAuthenticated = !token.isNullOrBlank()) }.let { flow -> kotlinx.coroutines.flow.first(flow) }
}

class ChatRepositoryImpl(private val api: EnalApi) : ChatRepository {
    override suspend fun sendMessage(request: ChatRequest) = runCatching {
        val response = api.sendChat(request)
        if (response.isSuccessful) response.body() ?: throw IllegalStateException("Empty chat body") else throw IllegalStateException(response.errorBody()?.string())
    }
}

class ObservabilityRepositoryImpl(private val api: EnalApi) : ObservabilityRepository {
    override suspend fun getLogs() = runCatching { api.logs().body() ?: emptyMap() }
    override suspend fun getTraces() = runCatching { api.traces().body() ?: emptyMap() }
}
