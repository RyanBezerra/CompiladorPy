package mini_compiler;

import lexical.Scanner;
import lexical.Token;

public class Main {
	
	public static void main(String[] args) {
		Scanner sc = new Scanner("programa.mc");
		Token tk;
		while ((tk = sc.nextToken()) != null) {
			System.out.println(tk);
		}
	}

}
