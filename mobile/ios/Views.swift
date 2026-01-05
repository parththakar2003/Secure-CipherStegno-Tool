import SwiftUI

struct MainTabView: View {
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            CryptoView()
                .tabItem {
                    Label("Crypto", systemImage: "lock.shield")
                }
                .tag(0)
            
            SteganographyView()
                .tabItem {
                    Label("Stego", systemImage: "photo")
                }
                .tag(1)
            
            ToolsView()
                .tabItem {
                    Label("Tools", systemImage: "wrench.and.screwdriver")
                }
                .tag(2)
            
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
                .tag(3)
        }
        .accentColor(.blue)
    }
}

struct CryptoView: View {
    @State private var selectedAlgorithm = "caesar"
    @State private var inputText = ""
    @State private var outputText = ""
    @State private var keyText = ""
    @State private var shiftValue = 3
    @State private var isEncrypting = true
    @State private var isLoading = false
    
    let algorithms = ["caesar", "vigenere", "aes", "rsa"]
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Algorithm picker
                    Picker("Algorithm", selection: $selectedAlgorithm) {
                        ForEach(algorithms, id: \.self) { algo in
                            Text(algo.uppercased()).tag(algo)
                        }
                    }
                    .pickerStyle(SegmentedPickerStyle())
                    .padding()
                    
                    // Mode toggle
                    Picker("Mode", selection: $isEncrypting) {
                        Text("Encrypt").tag(true)
                        Text("Decrypt").tag(false)
                    }
                    .pickerStyle(SegmentedPickerStyle())
                    .padding(.horizontal)
                    
                    // Input text
                    VStack(alignment: .leading) {
                        Text("Input Text")
                            .font(.headline)
                        TextEditor(text: $inputText)
                            .frame(height: 150)
                            .padding(4)
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(Color.gray, lineWidth: 1)
                            )
                    }
                    .padding(.horizontal)
                    
                    // Key/Password field
                    if selectedAlgorithm != "caesar" {
                        VStack(alignment: .leading) {
                            Text(selectedAlgorithm == "caesar" ? "Shift Value" : "Key/Password")
                                .font(.headline)
                            SecureField("Enter key", text: $keyText)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                        }
                        .padding(.horizontal)
                    } else {
                        VStack(alignment: .leading) {
                            Text("Shift Value: \(shiftValue)")
                                .font(.headline)
                            Slider(value: Binding(
                                get: { Double(shiftValue) },
                                set: { shiftValue = Int($0) }
                            ), in: 1...25, step: 1)
                        }
                        .padding(.horizontal)
                    }
                    
                    // Process button
                    Button(action: processText) {
                        HStack {
                            if isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            }
                            Text(isEncrypting ? "Encrypt" : "Decrypt")
                                .fontWeight(.semibold)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                    }
                    .disabled(isLoading || inputText.isEmpty)
                    .padding(.horizontal)
                    
                    // Output text
                    if !outputText.isEmpty {
                        VStack(alignment: .leading) {
                            HStack {
                                Text("Output")
                                    .font(.headline)
                                Spacer()
                                Button(action: copyOutput) {
                                    Label("Copy", systemImage: "doc.on.doc")
                                        .font(.caption)
                                }
                            }
                            Text(outputText)
                                .padding()
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(Color.gray.opacity(0.1))
                                .cornerRadius(8)
                        }
                        .padding(.horizontal)
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("Cryptography")
        }
    }
    
    func processText() {
        isLoading = true
        
        Task {
            do {
                if isEncrypting {
                    outputText = try await CryptoService.shared.encrypt(
                        text: inputText,
                        algorithm: selectedAlgorithm,
                        key: keyText,
                        shift: shiftValue
                    )
                } else {
                    outputText = try await CryptoService.shared.decrypt(
                        text: inputText,
                        algorithm: selectedAlgorithm,
                        key: keyText,
                        shift: shiftValue
                    )
                }
            } catch {
                outputText = "Error: \(error.localizedDescription)"
            }
            isLoading = false
        }
    }
    
    func copyOutput() {
        UIPasteboard.general.string = outputText
    }
}

struct SteganographyView: View {
    @State private var selectedImage: UIImage?
    @State private var messageText = ""
    @State private var isShowingImagePicker = false
    @State private var isEncoding = true
    @State private var resultMessage = ""
    @State private var isLoading = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Mode picker
                    Picker("Mode", selection: $isEncoding) {
                        Text("Hide Message").tag(true)
                        Text("Extract Message").tag(false)
                    }
                    .pickerStyle(SegmentedPickerStyle())
                    .padding()
                    
                    // Image selection
                    if let image = selectedImage {
                        Image(uiImage: image)
                            .resizable()
                            .scaledToFit()
                            .frame(height: 200)
                            .cornerRadius(10)
                    } else {
                        Rectangle()
                            .fill(Color.gray.opacity(0.3))
                            .frame(height: 200)
                            .overlay(
                                Text("No image selected")
                                    .foregroundColor(.gray)
                            )
                            .cornerRadius(10)
                    }
                    
                    Button(action: { isShowingImagePicker = true }) {
                        Label("Select Image", systemImage: "photo.on.rectangle")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue.opacity(0.1))
                            .foregroundColor(.blue)
                            .cornerRadius(10)
                    }
                    .padding(.horizontal)
                    
                    // Message input (only for encoding)
                    if isEncoding {
                        VStack(alignment: .leading) {
                            Text("Message to Hide")
                                .font(.headline)
                            TextEditor(text: $messageText)
                                .frame(height: 120)
                                .padding(4)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 8)
                                        .stroke(Color.gray, lineWidth: 1)
                                )
                        }
                        .padding(.horizontal)
                    }
                    
                    // Process button
                    Button(action: processSteganography) {
                        HStack {
                            if isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            }
                            Text(isEncoding ? "Hide Message" : "Extract Message")
                                .fontWeight(.semibold)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                    }
                    .disabled(isLoading || selectedImage == nil || (isEncoding && messageText.isEmpty))
                    .padding(.horizontal)
                    
                    // Result
                    if !resultMessage.isEmpty {
                        VStack(alignment: .leading) {
                            Text("Result")
                                .font(.headline)
                            Text(resultMessage)
                                .padding()
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(Color.gray.opacity(0.1))
                                .cornerRadius(8)
                        }
                        .padding(.horizontal)
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("Steganography")
            .sheet(isPresented: $isShowingImagePicker) {
                ImagePicker(image: $selectedImage)
            }
        }
    }
    
    func processSteganography() {
        guard let image = selectedImage else { return }
        isLoading = true
        
        Task {
            do {
                if isEncoding {
                    let result = try await SteganographyService.shared.encode(
                        image: image,
                        message: messageText
                    )
                    selectedImage = result
                    resultMessage = "Message successfully hidden! Save the image."
                } else {
                    let extractedMessage = try await SteganographyService.shared.decode(image: image)
                    resultMessage = "Extracted: \(extractedMessage)"
                }
            } catch {
                resultMessage = "Error: \(error.localizedDescription)"
            }
            isLoading = false
        }
    }
}

struct ToolsView: View {
    @State private var passwordInput = ""
    @State private var passwordStrength = ""
    @State private var generatedPassword = ""
    @State private var passwordLength = 16.0
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Password Validator")) {
                    TextField("Enter password", text: $passwordInput)
                    
                    Button("Validate") {
                        validatePassword()
                    }
                    
                    if !passwordStrength.isEmpty {
                        Text(passwordStrength)
                            .font(.caption)
                    }
                }
                
                Section(header: Text("Password Generator")) {
                    VStack(alignment: .leading) {
                        Text("Length: \(Int(passwordLength))")
                        Slider(value: $passwordLength, in: 8...32, step: 1)
                    }
                    
                    Button("Generate") {
                        generatePassword()
                    }
                    
                    if !generatedPassword.isEmpty {
                        HStack {
                            Text(generatedPassword)
                                .font(.system(.body, design: .monospaced))
                            Spacer()
                            Button(action: {
                                UIPasteboard.general.string = generatedPassword
                            }) {
                                Image(systemName: "doc.on.doc")
                            }
                        }
                    }
                }
                
                Section(header: Text("File Hash")) {
                    Button("Calculate File Hash") {
                        // Implementation
                    }
                }
            }
            .navigationTitle("Security Tools")
        }
    }
    
    func validatePassword() {
        Task {
            do {
                let result = try await APIClient.shared.validatePassword(passwordInput)
                passwordStrength = "Strength: \(result.strength) (Score: \(result.score)/8)"
            } catch {
                passwordStrength = "Error validating"
            }
        }
    }
    
    func generatePassword() {
        Task {
            do {
                let result = try await APIClient.shared.generatePassword(length: Int(passwordLength))
                generatedPassword = result.password
            } catch {
                generatedPassword = "Error generating"
            }
        }
    }
}

struct SettingsView: View {
    @AppStorage("apiEndpoint") private var apiEndpoint = "https://api.cipherstegno.com"
    @AppStorage("enableBiometrics") private var enableBiometrics = true
    @AppStorage("autoSave") private var autoSave = false
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("API Settings")) {
                    TextField("API Endpoint", text: $apiEndpoint)
                }
                
                Section(header: Text("Security")) {
                    Toggle("Biometric Authentication", isOn: $enableBiometrics)
                    Toggle("Auto-save Results", isOn: $autoSave)
                }
                
                Section(header: Text("About")) {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("3.1.0")
                            .foregroundColor(.gray)
                    }
                    
                    Link("GitHub Repository", destination: URL(string: "https://github.com/parththakar2003/Secure-CipherStegno-Tool")!)
                }
                
                Section {
                    Button("Sign Out", role: .destructive) {
                        // Sign out logic
                    }
                }
            }
            .navigationTitle("Settings")
        }
    }
}

struct AuthenticationView: View {
    @EnvironmentObject var authManager: BiometricAuthManager
    
    var body: some View {
        VStack(spacing: 30) {
            Image(systemName: "lock.shield.fill")
                .font(.system(size: 80))
                .foregroundColor(.blue)
            
            Text("Secure CipherStegno")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Authenticate to continue")
                .font(.subheadline)
                .foregroundColor(.gray)
            
            Button(action: {
                authManager.authenticate()
            }) {
                Label("Authenticate", systemImage: "faceid")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
            .padding(.horizontal, 40)
        }
    }
}

// Image Picker
struct ImagePicker: UIViewControllerRepresentable {
    @Binding var image: UIImage?
    @Environment(\.presentationMode) var presentationMode
    
    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: ImagePicker
        
        init(_ parent: ImagePicker) {
            self.parent = parent
        }
        
        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.image = image
            }
            parent.presentationMode.wrappedValue.dismiss()
        }
    }
}
