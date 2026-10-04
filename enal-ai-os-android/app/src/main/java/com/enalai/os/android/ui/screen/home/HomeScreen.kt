package com.enalai.os.android.ui.screen.home

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
fun HomeScreen(navController: NavController) {
    androidx.compose.foundation.layout.Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(text = "Enal AI OS")
        Button(onClick = { navController.navigate("chat") }, modifier = Modifier.fillMaxWidth()) { Text("Chat") }
        Button(onClick = { navController.navigate("observability") }, modifier = Modifier.fillMaxWidth()) { Text("Observability") }
        Button(onClick = { navController.navigate("settings") }, modifier = Modifier.fillMaxWidth()) { Text("Settings") }
    }
}
