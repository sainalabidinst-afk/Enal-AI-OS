package com.enalai.os.android.di

import android.content.Context
import com.enalai.os.android.data.local.SessionStore
import com.enalai.os.android.data.remote.EnalApi
import com.enalai.os.android.data.remote.RemoteModule
import com.enalai.os.android.data.repository.AuthRepository
import com.enalai.os.android.data.repository.AuthRepositoryImpl
import com.enalai.os.android.data.repository.ChatRepository
import com.enalai.os.android.data.repository.ChatRepositoryImpl
import com.enalai.os.android.data.repository.ObservabilityRepository
import com.enalai.os.android.data.repository.ObservabilityRepositoryImpl
import com.enalai.os.android.domain.usecase.LoginUseCase
import com.enalai.os.android.domain.usecase.ObserveAuthUseCase
import com.enalai.os.android.domain.usecase.SendChatUseCase

object ServiceLocator {
    lateinit var context: Context
        private set

    fun init(context: Context) {
        this.context = context.applicationContext
    }

    val api: EnalApi by lazy { RemoteModule.createApi() }
    val sessionStore: SessionStore by lazy { SessionStore(context) }
    val authRepository: AuthRepository by lazy { AuthRepositoryImpl(api, sessionStore) }
    val chatRepository: ChatRepository by lazy { ChatRepositoryImpl(api) }
    val observabilityRepository: ObservabilityRepository by lazy { ObservabilityRepositoryImpl(api) }
    val loginUseCase: LoginUseCase by lazy { LoginUseCase(authRepository) }
    val observeAuthUseCase: ObserveAuthUseCase by lazy { ObserveAuthUseCase(authRepository) }
    val sendChatUseCase: SendChatUseCase by lazy { SendChatUseCase(chatRepository) }
}
