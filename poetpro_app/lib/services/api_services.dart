import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:5000';
  //static const String baseUrl = 'http://10.65.85.150:5000';


  // ================= REGISTER =================
  static Future<Map<String, dynamic>> register(
    String username,
    String email,
    String password,
  ) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/register'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'username': username,
              'email': email,
              'password': password,
            }),
          )
          .timeout(const Duration(seconds: 60));

      return jsonDecode(response.body);
    } on SocketException {
      return {'message': 'Cannot connect to server'};
    } on FormatException {
      return {'message': 'Invalid server response'};
    } catch (e) {
      return {'message': 'Error: $e'};
    }
  }

  // ================= LOGIN =================
  static Future<Map<String, dynamic>> login(
    String email,
    String password,
  ) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/login'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'email': email, 'password': password}),
          )
          .timeout(const Duration(seconds: 60));

      return jsonDecode(response.body);
    } on SocketException {
      return {'message': 'Cannot connect to server'};
    } on FormatException {
      return {'message': 'Invalid server response'};
    } catch (e) {
      return {'message': 'Error: $e'};
    }
  }

  // ================= ANALYZE =================
  static Future<Map<String, dynamic>> analyze(
    String text,
    String poemType,
  ) async {
    try {
      final endpoint = poemType == 'pantun'
          ? '/pantun/analyze'
          : '/syair/analyze';

      final response = await http
          .post(
            Uri.parse('$baseUrl$endpoint'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'text': text}),
          )
          .timeout(const Duration(seconds: 60));

      return jsonDecode(response.body);
    } on SocketException {
      return {'message': 'Cannot connect to server'};
    } on FormatException {
      return {'message': 'Invalid server response'};
    } catch (e) {
      return {'message': 'Error: $e'};
    }
  }
}
