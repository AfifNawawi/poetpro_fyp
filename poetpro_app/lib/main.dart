import 'package:flutter/material.dart';
import 'pages/login_page.dart';

void main() => runApp(const PoetProApp());

class PoetProApp extends StatelessWidget {
  const PoetProApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'PoetPro',
      theme: ThemeData(primarySwatch: Colors.green),
      home: const LoginPage(),
    );
  }
}
