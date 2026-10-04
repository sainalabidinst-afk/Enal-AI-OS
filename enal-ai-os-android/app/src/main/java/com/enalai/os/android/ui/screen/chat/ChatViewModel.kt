package com.enalai.os.android.ui.screen.chat

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.enalai.os.android.data.remote.dto.ChatRequest
import com.enalai.os.android.domain.usecase.SendChatUseCase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class ChatMessage(
    val id: String,
    val text: String,
    val isUser: Boolean,
    val agent: String? = null,
    val timestamp: Long = System.currentTimeMillis()
)

data class ChatState(
    val messages: List<ChatMessage> = emptyList(),
    val inputMessage: String = "",
    val loading: Boolean = false,
    val error: String? = null,
    val conversationId: String? = null
)

class ChatViewModel(private val sendChatUseCase: SendChatUseCase) : ViewModel() {
    private val _state = MutableStateFlow(ChatState())
    val state: StateFlow<ChatState> = _state

    fun onInputChanged(input: String) {
        _state.value = _state.value.copy(inputMessage = input)
    }

    fun sendMessage() {
        val currentInput = _state.value.inputMessage.trim()
        if (currentInput.isEmpty() || _state.value.loading) return

        val userMessage = ChatMessage(
            id = System.currentTimeMillis().toString(),
            text = currentInput,
            isUser = true
        )

        _state.value = _state.value.copy(
            messages = _state.value.messages + userMessage,
            inputMessage = "",
            loading = true,
            error = null
        )

        viewModelScope.launch {
            val request = ChatRequest(
                message = currentInput,
                conversationId = _state.value.conversationId
            )
            val result = sendChatUseCase(request)
            result.onSuccess { response ->
                val botMessage = ChatMessage(
                    id = (System.currentTimeMillis() + 1).toString(),
                    text = response.message,
                    isUser = false,
                    agent = response.agent
                )
                _state.value = _state.value.copy(
                    messages = _state.value.messages + botMessage,
                    loading = false,
                    conversationId = response.conversationId
                )
            }.onFailure { throwable ->
                _state.value = _state.value.copy(
                    loading = false,
                    error = throwable.message ?: "Failed to send message"
                )
            }
        }
    }
}
