using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BulletBehaviour : MonoBehaviour
{
    private GameObject hero;
    // Start is called before the first frame update
    void Start()
    {
        hero =  GameObject.Find("Hero"); 
    }

    // Update is called once per frame
    void Update()
    {
        if (Vector3.Distance(hero.transform.position, transform.position) > 1)
            Destroy(gameObject);
    }
}
