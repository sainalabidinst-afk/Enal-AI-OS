package com.enalai.os.android.data.remote.dto

import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class AuthResponse(
    @Json(name = "access_token") val accessToken: String,
    @Json(name = "token_type") val tokenType: String = "bearer",
    @Json(name = "expires_in") val expiresIn: Int = 3600
)

@JsonClass(generateAdapter = true)
data class ChatRequest(
    val message: String,
    @Json(name = "conversation_id") val conversationId: String? = null,
    @Json(name = "workspace_id") val workspaceId: String? = null,
    val stream: Boolean = false
)

@JsonClass(generateAdapter = true)
data class ChatResponse(
    val message: String,
    @Json(name = "conversation_id") val conversationId: String,
    val agent: String,
    @Json(name = "tasks_completed") val tasksCompleted: Int = 0,
    val metadata: Map<String, Any> = emptyMap(),
    val analysis: Map<String, Any>? = null
)
