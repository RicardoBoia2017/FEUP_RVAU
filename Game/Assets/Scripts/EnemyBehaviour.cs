using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyBehaviour : MonoBehaviour
{
    private GameObject hero;
    private GameManager manager;
    private float speed = 0.3f;
    public int health;
    // Start is called before the first frame update
    public bool againstWall = false;
    void Start()
    {
        hero =  GameObject.Find("Hero");
        manager = GameObject.Find("Manager").GetComponent<GameManager>(); 
    }

    // Update is called once per frame
    void Update()
    {
        if(!againstWall)
            transform.position = Vector3.MoveTowards(transform.position, hero.transform.position + new Vector3(0,0.07f,0), speed * Time.deltaTime);
        else    
            transform.position += Vector3.right * speed/2 * Time.deltaTime;
    }

    void OnCollisionEnter(Collision c)
    {
        if(c.collider.gameObject.transform.tag == "Bullet")
        {
            health--;
            if(health <= 0)
            {
                Destroy(gameObject);
                manager.EnemyDown();
            }
            Destroy(c.collider.gameObject);
        }

        if(c.collider.gameObject.transform.tag == "Wall")
            againstWall = true;
    }

    void OnCollisionExit(Collision c)
    {
        if(c.collider.gameObject.transform.tag == "Wall")
            againstWall = false;
    }
}
