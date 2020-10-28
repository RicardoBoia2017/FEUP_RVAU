using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class ChangeText : MonoBehaviour
{
    private Text text;
    // Start is called before the first frame update
    void Start()
    {
        text = GameObject.Find("Coords").GetComponent<Text>();
    }

    // Update is called once per frame
    void Update()
    {
        text.text = transform.position.x.ToString() + ", " + 
                    transform.position.y.ToString() + ", " +
                    transform.position.z.ToString();
    }
}
