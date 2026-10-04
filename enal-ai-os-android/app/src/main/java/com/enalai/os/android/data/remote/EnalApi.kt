package com.enalai.os.android.data.remote

import com.enalai.os.android.data.remote.dto.AuthResponse
import com.enalai.os.android.data.remote.dto.ChatRequest
import com.enalai.os.android.data.remote.dto.ChatResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface EnalApi {
    @POST("auth/login")
    suspend fun login(@Body request: Map<String, String>): Response<AuthResponse>

    @POST("chat")
    suspend fun sendChat(@Body request: ChatRequest): Response<ChatResponse>

    @GET("observability/logs")
    suspend fun logs(): Response<Map<String, Any>>

    @GET("observability/trace")
    suspend fun traces(): Response<Map<String, Any>>
}
