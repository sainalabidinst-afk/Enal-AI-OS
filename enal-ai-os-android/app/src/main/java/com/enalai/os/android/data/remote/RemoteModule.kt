package com.enalai.os.android.data.remote

import com.enalai.os.android.data.remote.dto.AuthResponse
import com.enalai.os.android.data.remote.dto.ChatRequest
import com.enalai.os.android.data.remote.dto.ChatResponse
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory

object RemoteModule {
    private const val DEFAULT_BASE_URL = "http://localhost:8000/api/v1/"

    private val logging: HttpLoggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val client: OkHttpClient = OkHttpClient.Builder()
        .addInterceptor(logging)
        .build()

    fun createApi(baseUrl: String = DEFAULT_BASE_URL): EnalApi = Retrofit.Builder()
        .baseUrl(baseUrl)
        .client(client)
        .addConverterFactory(MoshiConverterFactory.create())
        .build()
        .create(EnalApi::class.java)
}
