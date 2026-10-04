package com.enalai.os.android.ui.screen.login

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController

@Composable
fun LoginScreen(navController: NavController, viewModel: LoginViewModel = androidx.lifecycle.viewmodel.compose.viewModel()) {
    val state by viewModel.state.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = "Enal AI OS")
        OutlinedTextField(value = state.username, onValueChange = viewModel::onUsernameChanged, label = { Text("Username") }, modifier = Modifier.fillMaxWidth())
        OutlinedTextField(value = state.password, onValueChange = viewModel::onPasswordChanged, label = { Text("Password") }, visualTransformation = PasswordVisualTransformation(), modifier = Modifier.fillMaxWidth())
        if (state.error != null) Text(text = state.error ?: "")
        Button(onClick = { viewModel.login { navController.navigate("home") { popUpTo("login") { inclusive = true } } }, enabled = !state.loading) {
            Text(text = if (state.loading) "Signing in..." else "Sign In")
        }
    }
}
