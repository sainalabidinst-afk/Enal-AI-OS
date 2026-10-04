package com.enalai.os.android.performance

import android.os.SystemClock
import java.util.concurrent.ConcurrentHashMap

object PerformanceMonitor {
    private val markers = ConcurrentHashMap<String, Long>()

    fun markStart(key: String) {
        markers[key] = SystemClock.elapsedRealtimeNanos()
    }

    fun markEnd(key: String): Long {
        val start = markers.remove(key) ?: return -1
        return (SystemClock.elapsedRealtimeNanos() - start) / 1_000_000
    }
}
