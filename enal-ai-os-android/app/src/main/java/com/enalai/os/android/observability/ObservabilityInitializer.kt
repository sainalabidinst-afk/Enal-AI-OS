package com.enalai.os.android.observability

import android.content.Context
import android.os.Build
import android.util.Log

object ObservabilityInitializer {
    fun init(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            Log.i("Observability", "Native tracing initialized")
        }
    }
}
