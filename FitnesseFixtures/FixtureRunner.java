package things2dofixtures;

import java.util.List;

public class FixtureRunner {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		ItemsNear IN = new ItemsNear("Recreational", 42.691, -71.128);
		
		List<Object> foo = IN.query();

	}

}
