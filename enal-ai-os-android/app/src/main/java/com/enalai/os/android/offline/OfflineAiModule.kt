package com.enalai.os.android.offline

import android.content.Context
import java.io.File

class OfflineAiModule(private val context: Context) {
    fun modelCacheDir(): File = File(context.filesDir, "offline_models").apply { mkdirs() }

    fun warmUpCache() {
        val dir = modelCacheDir()
        if (!dir.exists()) dir.mkdirs()
    }
}
