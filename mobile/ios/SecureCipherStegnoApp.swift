import SwiftUI

@main
struct SecureCipherStegnoApp: App {
    @StateObject private var appState = AppState()
    @StateObject private var authManager = BiometricAuthManager()
    
    var body: some Scene {
        WindowGroup {
            if authManager.isAuthenticated {
                MainTabView()
                    .environmentObject(appState)
            } else {
                AuthenticationView()
                    .environmentObject(authManager)
            }
        }
    }
}

class AppState: ObservableObject {
    @Published var currentUser: User?
    @Published var apiToken: String?
    
    init() {
        loadUserFromKeychain()
    }
    
    func loadUserFromKeychain() {
        // Load from keychain
        if let token = KeychainService.shared.getToken() {
            self.apiToken = token
        }
    }
}

struct User: Codable, Identifiable {
    let id: String
    let username: String
    let email: String
    let subscription: String
}
