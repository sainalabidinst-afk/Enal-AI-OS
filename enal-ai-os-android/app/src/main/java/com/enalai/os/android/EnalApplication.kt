package com.enalai.os.android

import android.app.Application
import android.util.Log
import androidx.work.Configuration
import com.enalai.os.android.observability.ObservabilityInitializer

class EnalApplication : Application(), Configuration.Provider {
    override fun onCreate() {
        super.onCreate()
        ObservabilityInitializer.init(this)
        Log.i("EnalApplication", "Stage 3 bootstrap complete")
    }

    override fun getWorkManagerConfiguration(): Configuration =
        Configuration.Builder()
            .setMinimumLoggingLevel(Log.DEBUG)
            .build()
}
