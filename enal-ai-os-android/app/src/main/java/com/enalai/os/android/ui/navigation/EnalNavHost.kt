package com.enalai.os.android.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.enalai.os.android.ui.screen.chat.ChatScreen
import com.enalai.os.android.ui.screen.home.HomeScreen
import com.enalai.os.android.ui.screen.login.LoginScreen
import com.enalai.os.android.ui.screen.observability.ObservabilityScreen
import com.enalai.os.android.ui.screen.settings.SettingsScreen

@Composable
fun EnalNavHost(navController: NavHostController = androidx.navigation.compose.rememberNavController()) {
    NavHost(navController = navController, startDestination = "login") {
        composable("login") { LoginScreen(navController) }
        composable("home") { HomeScreen(navController) }
        composable("chat") { ChatScreen(navController) }
        composable("observability") { ObservabilityScreen(navController) }
        composable("settings") { SettingsScreen(navController) }
    }
}
