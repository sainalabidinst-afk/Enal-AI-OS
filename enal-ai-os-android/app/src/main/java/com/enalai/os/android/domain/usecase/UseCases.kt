package com.enalai.os.android.domain.usecase

import com.enalai.os.android.data.remote.dto.ChatRequest
import com.enalai.os.android.data.remote.dto.ChatResponse
import com.enalai.os.android.domain.model.AuthState
import com.enalai.os.android.domain.repository.AuthRepository
import com.enalai.os.android.domain.repository.ChatRepository

class LoginUseCase(private val authRepository: AuthRepository) {
    suspend operator fun invoke(username: String, password: String) = authRepository.login(username, password)
}

class ObserveAuthUseCase(private val authRepository: AuthRepository) {
    operator fun invoke(): kotlinx.coroutines.flow.Flow<AuthState> = kotlinx.coroutines.flow.flow { emit(authRepository.currentAuth()) }
}

class SendChatUseCase(private val chatRepository: ChatRepository) {
    suspend operator fun invoke(request: ChatRequest) = chatRepository.sendMessage(request)
}
