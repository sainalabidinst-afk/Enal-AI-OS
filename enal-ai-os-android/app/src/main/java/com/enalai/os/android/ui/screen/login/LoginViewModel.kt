package com.enalai.os.android.ui.screen.login

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.enalai.os.android.data.remote.dto.AuthResponse
import com.enalai.os.android.domain.usecase.LoginUseCase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class LoginState(
    val username: String = "",
    val password: String = "",
    val loading: Boolean = false,
    val error: String? = null,
    val authenticated: Boolean = false
)

class LoginViewModel(private val loginUseCase: LoginUseCase) : ViewModel() {
    private val _state = MutableStateFlow(LoginState())
    val state: StateFlow<LoginState> = _state

    fun onUsernameChanged(username: String) { _state.value = _state.value.copy(username = username, error = null) }
    fun onPasswordChanged(password: String) { _state.value = _state.value.copy(password = password, error = null) }

    fun login(onSuccess: () -> Unit) {
        val current = _state.value
        if (current.username.isBlank() || current.password.isBlank()) {
            _state.value = current.copy(error = "Username and password are required")
            return
        }
        viewModelScope.launch {
            _state.value = current.copy(loading = true, error = null)
            val result = loginUseCase(current.username, current.password)
            result.onSuccess { response: AuthResponse ->
                _state.value = _state.value.copy(loading = false, authenticated = true)
                onSuccess()
            }.onFailure { throwable ->
                _state.value = _state.value.copy(loading = false, error = throwable.message ?: "Login failed")
            }
        }
    }
}
