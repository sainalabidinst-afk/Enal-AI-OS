package com.enalai.os.android.ui.screen.settings

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavController

@Composable
fun SettingsScreen(navController: NavController) {
    androidx.compose.foundation.layout.Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(text = "Settings")
        Button(onClick = { }, modifier = Modifier.fillMaxWidth()) { Text("Clear Cache") }
        Button(onClick = { navController.navigate("login") { popUpTo("home") { inclusive = true } } }, modifier = Modifier.fillMaxWidth()) { Text("Logout") }
    }
}
