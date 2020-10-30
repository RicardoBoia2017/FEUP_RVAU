using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HeroBehaviour : MonoBehaviour
{
    private Text text;
    public GameManager manager;
    public GameObject projectile;

    private bool invokerCalled = false;

    // Start is called before the first frame update
    void Start()
    {
        text = GameObject.Find("Distance").GetComponent<Text>();
    }

    void OnCollisionEnter(Collision c)
    {
        if(c.collider.gameObject.transform.tag == "Enemy")
        {
            manager.GameOver(c.collider.gameObject.transform.name);
        }
    }

    public void InvokeFireBullet()
    {
        if(!invokerCalled)
        {
            InvokeRepeating("FireBullet", 1f, 0.5f);
            invokerCalled = true;
        }
    }

    void FireBullet()
    {
        GameObject bullet = Instantiate(projectile, transform.position, Quaternion.identity) as GameObject;
        bullet.transform.Rotate(90f, 0f, 0f, Space.Self);
        bullet.GetComponent<Rigidbody>().AddForce(transform.forward * 30);
    }
}
